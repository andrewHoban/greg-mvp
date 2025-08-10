"""
Knowledge base service for loading and managing domain knowledge.
"""
import os
from typing import Dict, List
import yaml
from loguru import logger

from ..models.query_models import KnowledgeDomain, JoinRule


class KnowledgeBase:
    """Service for loading and accessing domain knowledge."""
    
    def __init__(self):
        self._domains: Dict[str, KnowledgeDomain] = {}
        self._load_domain_knowledge()
    
    def _load_domain_knowledge(self):
        """Load domain knowledge from YAML files."""
        domain_data_dir = os.path.join(os.path.dirname(__file__), "..", "domain_data")
        
        if not os.path.exists(domain_data_dir):
            logger.warning(f"Domain data directory not found: {domain_data_dir}")
            return
        
        for filename in os.listdir(domain_data_dir):
            if filename.endswith(('.yml', '.yaml')):
                filepath = os.path.join(domain_data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        data = yaml.safe_load(file)
                    
                    domain = KnowledgeDomain(
                        domain=data['domain'],
                        description=data.get('description', ''),
                        tables=data.get('tables', {}),
                        joins=[JoinRule(**join) for join in data.get('joins', [])],
                        business_rules=data.get('business_rules', []),
                        sample_questions=data.get('sample_questions', [])
                    )
                    
                    self._domains[domain.domain] = domain
                    logger.info(f"Loaded domain knowledge: {domain.domain}")
                    
                except Exception as e:
                    logger.error(f"Error loading domain knowledge from {filepath}: {e}")
    
    def get_all_domains(self) -> Dict[str, KnowledgeDomain]:
        """Get all loaded domain knowledge."""
        return self._domains.copy()
    
    def get_domain(self, domain_name: str) -> KnowledgeDomain:
        """Get specific domain knowledge."""
        if domain_name not in self._domains:
            raise ValueError(f"Domain '{domain_name}' not found")
        return self._domains[domain_name]
    
    def get_available_domains(self) -> List[str]:
        """Get list of available domain names."""
        return list(self._domains.keys())
    
    def get_schema_context(self) -> str:
        """Get formatted schema context for NL-to-SQL generation."""
        context_parts = []
        
        for domain_name, domain in self._domains.items():
            context_parts.append(f"DOMAIN: {domain_name.upper()}")
            context_parts.append(f"Description: {domain.description}")
            
            for table_name, table_info in domain.tables.items():
                context_parts.append(f"\nTable: {table_name}")
                context_parts.append(f"  Description: {table_info.get('description', '')}")
                
                for field in table_info.get('fields', []):
                    context_parts.append(
                        f"  - {field['name']} ({field['type']}): {field['description']}"
                    )
            
            if domain.joins:
                context_parts.append("\nAvailable Joins:")
                for join in domain.joins:
                    context_parts.append(f"  - {join.left_table} {join.join_type} JOIN {join.right_table} ON {join.join_condition}")
            
            context_parts.append("")
        
        return "\n".join(context_parts)