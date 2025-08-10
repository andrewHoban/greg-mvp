from .services.knowledge_base import KnowledgeBase
from .config import settings

_kb: KnowledgeBase | None = None

def get_kb() -> KnowledgeBase:
    global _kb
    if _kb is None:
        _kb = KnowledgeBase.from_yaml(settings.knowledge_file)
    return _kb
