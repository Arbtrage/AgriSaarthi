from typing import Optional
from app.agents.base_agent import BaseAgent
from app.agents.weather_agent.agent import WeatherAgent
from app.agents.crop_science_agent.agent import CropScienceAgent
from app.agents.market_agent.agent import MarketAgent
from app.agents.finance_agent.agent import FinanceAgent
from app.agents.soil_health_agent.agent import SoilHealthAgent
from app.agents.fertilizer_agent.agent import FertilizerAgent
from app.agents.gov_schemes_agent.agent import GovSchemesAgent
from app.agents.other_agent.agent import OtherAgent


class AgentFactory:
    """Factory class for creating specialized agricultural agents."""

    # Mapping of categories to agent classes
    AGENT_MAP = {
        # Primary categories
        "crop_info": CropScienceAgent,
        "fertilizers": FertilizerAgent,
        "market_prices": MarketAgent,
        "gov_schemes": GovSchemesAgent,
        "other": OtherAgent,
        # Additional categories for flexibility
        "weather_info": WeatherAgent,
        "market_info": MarketAgent,
        "finance_info": FinanceAgent,
        "soil_info": SoilHealthAgent,
        "weather": WeatherAgent,
        "crop": CropScienceAgent,
        "market": MarketAgent,
        "finance": FinanceAgent,
        "soil": SoilHealthAgent,
        "soil_health": SoilHealthAgent,
        "crop_science": CropScienceAgent,
        "fertilizer": FertilizerAgent,
        "government_schemes": GovSchemesAgent,
        "general": OtherAgent,
    }

    @classmethod
    def create_agent(
        cls, category: str, language: str = "en-IN", markdown: bool = False
    ) -> BaseAgent:
        """
        Create an agent based on the category, language, and markdown preference.

        Args:
            category: The category of agricultural information needed
            language: The language code for the agent (e.g., "hi-IN", "en-US")
            markdown: Whether the response should be formatted in markdown

        Returns:
            A specialized agent instance

        Raises:
            ValueError: If the category is not recognized
        """
        agent_class = cls.AGENT_MAP.get(category.lower())

        if agent_class is None:
            # Default to crop science agent if category is not recognized
            agent_class = CropScienceAgent
            print(
                f"Warning: Unknown category '{category}', defaulting to CropScienceAgent"
            )

        return agent_class(language=language, markdown=markdown)

    @classmethod
    def get_available_categories(cls) -> list:
        """Get list of available agent categories."""
        return list(cls.AGENT_MAP.keys())

    @classmethod
    def get_agent_description(cls, category: str) -> str:
        """Get a description of what each agent specializes in."""
        descriptions = {
            # Primary categories
            "crop_info": "Offers crop selection, management, and science-based farming advice",
            "fertilizers": "Provides fertilizer recommendations, application rates, and management practices",
            "market_prices": "Provides current market prices, trends, and selling strategies for agricultural products",
            "gov_schemes": "Provides information about government agricultural schemes, subsidies, and support programs",
            "other": "Provides general agricultural advice, farming tips, and miscellaneous farming topics",
            # Additional categories
            "weather_info": "Provides weather-related agricultural advice, forecasts, and climate information",
            "market_info": "Provides market prices, trends, and selling strategies for agricultural products",
            "finance_info": "Offers financial advice including loans, subsidies, and investment planning",
            "soil_info": "Provides soil health management, testing, and improvement recommendations",
        }
        return descriptions.get(category.lower(), "Agricultural information and advice")
