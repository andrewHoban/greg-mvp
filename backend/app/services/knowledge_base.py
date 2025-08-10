from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from backend.app.logging import get_logger_for_module

logger = get_logger_for_module(__name__)


class KnowledgeBase:
    """Knowledge base that loads and manages domain data from YAML files."""

    def __init__(self) -> None:
        """Initialize the knowledge base."""
        self.domains: Dict[str, Any] = {}
        self._load_domain_data()

    def _load_domain_data(self) -> None:
        """Load domain data from YAML files in the domain_data directory."""
        domain_data_path = Path(__file__).parent.parent / "domain_data"

        if not domain_data_path.exists():
            logger.warning(f"Domain data directory not found: {domain_data_path}")
            return

        logger.info(f"Loading domain data from: {domain_data_path}")

        # Load all YAML files in the domain_data directory
        for yaml_file in domain_data_path.glob("*.yml"):
            try:
                with open(yaml_file, encoding='utf-8') as file:
                    domain_data = yaml.safe_load(file)
                    domain_name = yaml_file.stem
                    self.domains[domain_name] = domain_data
                    logger.info(f"Loaded domain: {domain_name}")
            except Exception as e:
                logger.error(f"Error loading {yaml_file}: {e}")

        logger.info(f"Loaded {len(self.domains)} domains")

    def list_domains(self) -> List[str]:
        """
        Get list of available domain names.
        
        Returns:
            List of domain names
        """
        return list(self.domains.keys())

    def get_domain(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get domain data by name.
        
        Args:
            name: Domain name
            
        Returns:
            Domain data dictionary or None if not found
        """
        return self.domains.get(name)

    def get_all_domains(self) -> Dict[str, Any]:
        """
        Get all domain data.
        
        Returns:
            Dictionary of all domains
        """
        return self.domains.copy()
