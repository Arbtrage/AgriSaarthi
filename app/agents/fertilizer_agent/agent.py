from app.agents.base_agent import BaseAgent
from app.agents.fertilizer_agent.prompt import FERTILIZER_PROMPT


class FertilizerAgent(BaseAgent):
    """Agent specialized in fertilizer recommendations and management."""

    def __init__(self, language: str = "en-US"):
        super().__init__(language=language)
        self.specialization = "fertilizer_management"
        self.prompt_template = FERTILIZER_PROMPT

    def get_agent_description(self) -> str:
        """Get description of what this agent specializes in."""
        return "Provides fertilizer recommendations, application rates, timing, and management practices for various crops and soil conditions"

    def get_specialized_tools(self):
        """Get tools specific to fertilizer management."""
        return [
            "fertilizer_calculator",
            "soil_test_analyzer",
            "crop_fertilizer_guide",
            "fertilizer_schedule_planner",
        ]
