import asyncio
import threading

class ThreadSafeEventBus:
    def __init__(self):
        self.queues = []
        self.lock = threading.Lock()
        self.loop = None

    def set_loop(self, loop):
        self.loop = loop

    def subscribe(self):
        q = asyncio.Queue()
        with self.lock:
            self.queues.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.queues:
                self.queues.remove(q)

    def publish(self, event: dict):
        with self.lock:
            for q in self.queues:
                if self.loop:
                    self.loop.call_soon_threadsafe(q.put_nowait, event)

bus = ThreadSafeEventBus()

def publish_event(event_type: str, data: dict):
    bus.publish({"type": event_type, **data})
