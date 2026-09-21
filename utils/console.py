"""Colour helpers for demo output."""

try:
    from dashboard.backend.event_bus import publish_event
except ImportError:
    def publish_event(event_type, data):
        pass

def _emit(level, text):
    publish_event("log", {"level": level, "message": text})

def title(text):
    print(f"\n{'=' * len(text)}\n{text}\n{'=' * len(text)}")
    _emit("title", text)

def step(text):
    print(f"  - {text}")
    _emit("step", text)

def danger(text):
    print(f"  [!]       {text}")
    _emit("danger", text)

def blocked(text):
    print(f"  [BLOCKED] {text}")
    _emit("blocked", text)

def ok(text):
    print(f"  [OK]      {text}")
    _emit("ok", text)

def bold(text):
    return text
