from typing import Optional, List
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import FunctionTool
from app.core.llm import get_llm
from app.agents.tools import build_vector_search_tool, build_web_search_tool


class BaseAgent:
    """Base class for all specialized agricultural agents."""

    def __init__(self, language: str = "en-US"):
        self.language = language
        self.tools = self._build_tools()
        self.system_prompt = self._build_system_prompt()
        self.agent = self._build_agent()

    def _build_tools(self) -> List[FunctionTool]:
        """Build the common tools that all agents use."""
        return [build_vector_search_tool(), build_web_search_tool()]

    def _build_system_prompt(self) -> str:
        """Build the base system prompt with language instruction."""
        language_instruction = self._get_language_instruction()

        base_prompt = f"""You are an agricultural AI assistant. {language_instruction}

You have access to two tools:
1. knowledge_base_search: Search the knowledge base for relevant agricultural information
2. web_search: Search the web for current information, market prices, weather updates, and news

Always use these tools to provide accurate, up-to-date information. When using retrieved information, cite the sources.

{self._get_agent_specific_prompt()}

Remember to respond in the user's preferred language: {self.language}"""

        return base_prompt

    def _get_language_instruction(self) -> str:
        """Get language-specific instruction based on the language code."""
        language_map = {
            "hi-IN": "आप हिंदी में बात करेंगे और किसानों की मदद करेंगे।",
            "en-US": "You will communicate in English and help farmers.",
            "pa-IN": "ਤੁਸੀਂ ਪੰਜਾਬੀ ਵਿੱਚ ਗੱਲ ਕਰੋਗੇ ਅਤੇ ਕਿਸਾਨਾਂ ਦੀ ਮਦਦ ਕਰੋਗੇ।",
            "bn-IN": "আপনি বাংলায় কথা বলবেন এবং কৃষকদের সাহায্য করবেন।",
            "ta-IN": "நீங்கள் தமிழில் பேசுவீர்கள் மற்றும் விவசாயிகளுக்கு உதவுவீர்கள்।",
            "te-IN": "మీరు తెలుగులో మాట్లాడతారు మరియు రైతులకు సహాయం చేస్తారు।",
            "mr-IN": "तुम्ही मराठीत बोलाल आणि शेतकऱ्यांना मदत कराल।",
            "gu-IN": "તમે ગુજરાતીમાં વાત કરશો અને કૃષકોને મદદ કરશો।",
            "kn-IN": "ನೀವು ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡುತ್ತೀರಿ ಮತ್ತು ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡುತ್ತೀರಿ।",
            "ml-IN": "നിങ്ങൾ മലയാളത്തിൽ സംസാരിക്കും കൂടാതെ കർഷകർക്ക് സഹായിക്കും।",
        }

        return language_map.get(
            self.language,
            "You will communicate in the user's preferred language and help farmers.",
        )

    def _get_agent_specific_prompt(self) -> str:
        """Override this method in subclasses to provide agent-specific instructions."""
        return ""

    def _build_agent(self) -> FunctionAgent:
        """Build the FunctionAgent with tools and system prompt."""
        return FunctionAgent(
            tools=self.tools,
            llm=get_llm(),
            system_prompt=self.system_prompt,
        )

    def get_agent(self) -> FunctionAgent:
        """Get the configured FunctionAgent."""
        return self.agent
