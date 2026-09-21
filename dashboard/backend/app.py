import sys
import os
import asyncio
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dashboard.backend.event_bus import bus
import demo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    bus.set_loop(asyncio.get_running_loop())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    q = bus.subscribe()
    try:
        while True:
            event = await q.get()
            await websocket.send_json(event)
    except WebSocketDisconnect:
        bus.unsubscribe(q)

@app.post("/api/scenario/{name}")
async def run_scenario(name: str):
    if name not in demo.SCENARIOS:
        return {"error": "Invalid scenario"}
    
    func = demo.SCENARIOS[name]
    if func is None:
        if name == "mitm":
            threading.Thread(target=demo.scenario_mitm, args=(True, 9210), daemon=True).start()
        elif name == "mitm_off":
            threading.Thread(target=demo.scenario_mitm, args=(False, 9220), daemon=True).start()
        elif name == "replay":
            threading.Thread(target=demo.scenario_replay, args=(True,), daemon=True).start()
    else:
        threading.Thread(target=func, daemon=True).start()
        
    return {"status": "started"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
