"""
Knowledge Base for loading domain data from YAML files
"""

import os
from typing import Dict, List, Optional
import yaml

from ..logging import get_logger
from ..models.query_models import KnowledgeDomain, TableDoc, FieldDoc, JoinRule

logger = get_logger(__name__)


class KnowledgeBase:
    """Knowledge base that loads domain data from YAML files."""
    
    def __init__(self) -> None:
        """Initialize the knowledge base."""
        self.domains: Dict[str, KnowledgeDomain] = {}
        self._load_domains()
    
    def _load_domains(self) -> None:
        """Load all domain data from YAML files."""
        domain_data_dir = os.path.join(
            os.path.dirname(__file__), "..", "domain_data"
        )
        
        if not os.path.exists(domain_data_dir):
            logger.warning(f"Domain data directory not found: {domain_data_dir}")
            return
        
        for filename in os.listdir(domain_data_dir):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                filepath = os.path.join(domain_data_dir, filename)
                try:
                    domain = self._load_domain_file(filepath)
                    if domain:
                        self.domains[domain.name] = domain
                        logger.info(f"Loaded domain: {domain.name}")
                except Exception as e:
                    logger.error(f"Failed to load domain file {filename}: {e}")
    
    def _load_domain_file(self, filepath: str) -> Optional[KnowledgeDomain]:
        """Load a single domain file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data:
            return None
        
        # Parse tables
        tables = []
        for table_data in data.get('tables', []):
            fields = [
                FieldDoc(**field_data) for field_data in table_data.get('fields', [])
            ]
            table = TableDoc(
                name=table_data['name'],
                description=table_data['description'],
                fields=fields
            )
            tables.append(table)
        
        # Parse joins
        joins = [
            JoinRule(**join_data) for join_data in data.get('joins', [])
        ]
        
        # Create domain
        domain = KnowledgeDomain(
            name=data['name'],
            description=data['description'],
            tables=tables,
            joins=joins,
            caveats=data.get('caveats', []),
            sample_questions=data.get('sample_questions', [])
        )
        
        return domain
    
    def get_domain_names(self) -> List[str]:
        """Get list of all domain names."""
        return list(self.domains.keys())
    
    def get_domain(self, domain_name: str) -> Optional[KnowledgeDomain]:
        """Get a specific domain by name."""
        return self.domains.get(domain_name)
    
    def get_all_domains(self) -> Dict[str, KnowledgeDomain]:
        """Get all domains."""
        return self.domains.copy()
    
    def search_tables(self, query: str) -> List[str]:
        """Search for tables matching the query across all domains."""
        results = []
        query_lower = query.lower()
        
        for domain in self.domains.values():
            for table in domain.tables:
                if (query_lower in table.name.lower() or 
                    query_lower in table.description.lower()):
                    results.append(f"{domain.name}.{table.name}")
        
        return results