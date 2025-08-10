"""Knowledge base service for managing domain YAML files."""

from __future__ import annotations

import os
from typing import Any

import yaml
from loguru import logger

from backend.app.models import DomainInfo


class KnowledgeBase:
    """Manages domain knowledge from YAML files."""

    def __init__(self, domains_path: str = "backend/domain"):
        self.domains_path = domains_path
        self.domains: dict[str, dict[str, Any]] = {}

    def load_domains(self) -> None:
        """Load all domain YAML files from the domains directory."""
        if not os.path.exists(self.domains_path):
            logger.warning(f"Domains path {self.domains_path} does not exist")
            return

        yaml_files = [f for f in os.listdir(self.domains_path) if f.endswith(".yaml")]
        logger.info(f"Loading {len(yaml_files)} domain files from {self.domains_path}")

        for yaml_file in yaml_files:
            file_path = os.path.join(self.domains_path, yaml_file)
            domain_name = yaml_file.replace(".yaml", "")

            try:
                with open(file_path, encoding="utf-8") as f:
                    domain_data = yaml.safe_load(f)
                    self.domains[domain_name] = domain_data
                    logger.info(f"Loaded domain: {domain_name}")
            except Exception as e:
                logger.error(f"Failed to load domain file {yaml_file}: {e}")

        logger.info(f"Successfully loaded {len(self.domains)} domains")

    def list_domains(self) -> list[DomainInfo]:
        """Return a list of all available domains."""
        domain_list = []

        for domain_name, domain_data in self.domains.items():
            domain_info = DomainInfo(
                name=domain_name,
                description=domain_data.get(
                    "description", f"{domain_name.title()} domain"
                ),
                tables=list(domain_data.get("tables", {}).keys()),
                sample_questions=domain_data.get("sample_questions", []),
            )
            domain_list.append(domain_info)

        return domain_list

    def get_domain(self, domain_name: str) -> DomainInfo | None:
        """Get detailed information for a specific domain."""
        if domain_name not in self.domains:
            return None

        domain_data = self.domains[domain_name]
        return DomainInfo(
            name=domain_name,
            description=domain_data.get("description", f"{domain_name.title()} domain"),
            tables=list(domain_data.get("tables", {}).keys()),
            sample_questions=domain_data.get("sample_questions", []),
        )

    def get_domain_schema(self, domain_name: str) -> dict[str, Any]:
        """Get the detailed schema for a domain."""
        if domain_name not in self.domains:
            return {}

        return self.domains[domain_name].get("tables", {})

    def find_relevant_domains(self, question: str) -> list[str]:
        """Find domains that might be relevant to the given question."""
        relevant_domains = []
        question_lower = question.lower()

        # Simple keyword matching - in production this would be more sophisticated
        keywords_map = {
            "financials": [
                "revenue",
                "money",
                "payment",
                "transaction",
                "financial",
                "profit",
                "cost",
            ],
            "customer_care": [
                "customer",
                "support",
                "ticket",
                "issue",
                "complaint",
                "satisfaction",
            ],
            "reads": ["engagement", "content", "article", "read", "view", "user"],
        }

        for domain_name in self.domains:
            # Check if domain name is mentioned
            if domain_name in question_lower:
                relevant_domains.append(domain_name)
                continue

            # Check keywords
            if domain_name in keywords_map:
                if any(
                    keyword in question_lower for keyword in keywords_map[domain_name]
                ):
                    relevant_domains.append(domain_name)

        return (
            relevant_domains if relevant_domains else ["financials"]
        )  # Default to financials
