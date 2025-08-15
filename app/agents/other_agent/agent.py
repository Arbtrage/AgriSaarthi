from app.agents.base_agent import BaseAgent
from app.agents.other_agent.prompt import OTHER_PROMPT


class OtherAgent(BaseAgent):
    """Agent specialized in miscellaneous agricultural topics and general farming advice."""

    def __init__(self, language: str = "en-US"):
        super().__init__(language=language)
        self.specialization = "general_agriculture"
        self.prompt_template = OTHER_PROMPT

    def get_agent_description(self) -> str:
        """Get description of what this agent specializes in."""
        return "Provides general agricultural advice, farming tips, and information on miscellaneous farming topics not covered by other specialized agents"

    def get_specialized_tools(self):
        """Get tools specific to general agriculture."""
        return [
            "farming_tips_generator",
            "agricultural_calendar",
            "best_practices_guide",
            "problem_solver",
            "resource_finder",
        ]
