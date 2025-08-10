import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional


class KnowledgeBase:
    """Domain knowledge loader from YAML files."""
    
    def __init__(self, domain_data_path: str = "backend/app/domain_data"):
        self.domain_data_path = Path(domain_data_path)
        self._domains = None
    
    def list_domains(self) -> List[str]:
        """List available knowledge domains."""
        if self._domains is None:
            self._load_domains()
        return list(self._domains.keys())
    
    def get_domain(self, name: str) -> Optional[Dict[str, Any]]:
        """Get domain knowledge by name."""
        if self._domains is None:
            self._load_domains()
        return self._domains.get(name)
    
    def _load_domains(self):
        """Load all domain YAML files."""
        self._domains = {}
        
        if not self.domain_data_path.exists():
            return
        
        for yaml_file in self.domain_data_path.glob("*.yml"):
            domain_name = yaml_file.stem
            try:
                with open(yaml_file, 'r') as f:
                    domain_data = yaml.safe_load(f)
                    self._domains[domain_name] = domain_data
            except Exception as e:
                print(f"Error loading domain {domain_name}: {e}")
                continue