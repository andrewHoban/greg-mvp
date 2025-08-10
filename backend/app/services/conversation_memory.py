import uuid
from collections import defaultdict, deque

# Simple in-memory conversation store for continuity
# conversation_id -> deque of messages
_memory: dict[str, deque] = defaultdict(lambda: deque(maxlen=10))

def append_message(conversation_id: str, role: str, content: str):
    _memory[conversation_id].append({"role": role, "content": content})

def get_conversation(conversation_id: str):
    return list(_memory[conversation_id])

def ensure_conversation(conversation_id: str | None) -> str:
    if conversation_id is None:
        return str(uuid.uuid4())
    return conversation_id
