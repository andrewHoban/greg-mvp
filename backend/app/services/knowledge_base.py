import yaml
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class Table:
    name: str
    columns: List[str]

class KnowledgeBase:
    def __init__(self, tables: List[Table]) -> None:
        self.tables = {t.name: t for t in tables}

    @classmethod
    def from_yaml(cls, path: str) -> "KnowledgeBase":
        with open(path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f)
        tables = [Table(name=t["name"], columns=t["columns"]) for t in data.get("tables", [])]
        return cls(tables)

    def list_tables(self) -> List[str]:
        return list(self.tables.keys())

    def describe(self) -> Dict[str, List[str]]:
        return {name: t.columns for name, t in self.tables.items()}
