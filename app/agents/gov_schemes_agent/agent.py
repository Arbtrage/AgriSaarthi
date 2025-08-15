from app.agents.base_agent import BaseAgent
from app.agents.gov_schemes_agent.prompt import GOV_SCHEMES_PROMPT


class GovSchemesAgent(BaseAgent):
    """Agent specialized in government agricultural schemes and subsidies."""

    def __init__(self, language: str = "en-US"):
        super().__init__(language=language)
        self.specialization = "government_schemes"
        self.prompt_template = GOV_SCHEMES_PROMPT

    def get_agent_description(self) -> str:
        """Get description of what this agent specializes in."""
        return "Provides information about government agricultural schemes, subsidies, loans, and support programs for farmers"

    def get_specialized_tools(self):
        """Get tools specific to government schemes."""
        return [
            "scheme_finder",
            "eligibility_checker",
            "application_guide",
            "subsidy_calculator",
            "document_requirements",
        ]
