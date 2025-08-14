from typing import Optional
from app.agents.base_agent import BaseAgent
from app.agents.weather_agent.agent import WeatherAgent
from app.agents.crop_science_agent.agent import CropScienceAgent
from app.agents.market_agent.agent import MarketAgent
from app.agents.finance_agent.agent import FinanceAgent
from app.agents.soil_health_agent.agent import SoilHealthAgent


class AgentFactory:
    """Factory class for creating specialized agricultural agents."""

    # Mapping of categories to agent classes
    AGENT_MAP = {
        "weather_info": WeatherAgent,
        "crop_info": CropScienceAgent,
        "market_info": MarketAgent,
        "finance_info": FinanceAgent,
        "soil_info": SoilHealthAgent,
        # Alternative category names for flexibility
        "weather": WeatherAgent,
        "crop": CropScienceAgent,
        "market": MarketAgent,
        "finance": FinanceAgent,
        "soil": SoilHealthAgent,
        "soil_health": SoilHealthAgent,
        "crop_science": CropScienceAgent,
    }

    @classmethod
    def create_agent(cls, category: str, language: str = "en-US") -> BaseAgent:
        """
        Create an agent based on the category and language.

        Args:
            category: The category of agricultural information needed
            language: The language code for the agent (e.g., "hi-IN", "en-US")

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

        return agent_class(language=language)

    @classmethod
    def get_available_categories(cls) -> list:
        """Get list of available agent categories."""
        return list(cls.AGENT_MAP.keys())

    @classmethod
    def get_agent_description(cls, category: str) -> str:
        """Get a description of what each agent specializes in."""
        descriptions = {
            "weather_info": "Provides weather-related agricultural advice, forecasts, and climate information",
            "crop_info": "Offers crop selection, management, and science-based farming advice",
            "market_info": "Provides market prices, trends, and selling strategies for agricultural products",
            "finance_info": "Offers financial advice including loans, subsidies, and investment planning",
            "soil_info": "Provides soil health management, testing, and improvement recommendations",
        }
        return descriptions.get(category.lower(), "Agricultural information and advice")
