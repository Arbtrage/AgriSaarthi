# AgriSaarthi Modular Agent System

This document describes the modular agent system for AgriSaarthi, which provides specialized agricultural advice through five different AI agents.

## Overview

The system consists of five specialized agents, each focusing on a specific area of agricultural expertise:

1. **Weather Agent** - Weather-related agricultural advice and forecasts
2. **Crop Science Agent** - Crop selection, management, and scientific farming advice
3. **Market Agent** - Market prices, trends, and selling strategies
4. **Finance Agent** - Financial advice, loans, subsidies, and investment planning
5. **Soil Health Agent** - Soil management, testing, and improvement recommendations

## Architecture

### Directory Structure

```
app/agents/
├── base_agent.py              # Base class for all agents
├── agent_factory.py           # Factory for creating agents
├── tools.py                   # Shared tools (knowledge base + web search)
├── weather_agent/             # Weather Agent implementation
│   ├── __init__.py
│   ├── agent.py
│   └── prompt.py
├── crop_science_agent/        # Crop Science Agent implementation
│   ├── __init__.py
│   ├── agent.py
│   └── prompt.py
├── market_agent/              # Market Agent implementation
│   ├── __init__.py
│   ├── agent.py
│   └── prompt.py
├── finance_agent/             # Finance Agent implementation
│   ├── __init__.py
│   ├── agent.py
│   └── prompt.py
└── soil_health_agent/         # Soil Health Agent implementation
    ├── __init__.py
    ├── agent.py
    └── prompt.py
```

### Key Components

#### BaseAgent Class

- Provides common functionality for all agents
- Handles language-specific instructions
- Manages shared tools (knowledge base search + web search)
- Builds system prompts with agent-specific expertise

#### AgentFactory

- Creates the appropriate agent based on category
- Maps category strings to agent classes
- Provides fallback to default agent if category is unknown

#### Shared Tools

- **knowledge_base_search**: Searches the Milvus vector database for agricultural information
- **web_search**: Searches the web for current information, market prices, and news

## API Usage

### New Chat Endpoint

The main chat endpoint now accepts a JSON body with the following structure:

```json
{
  "language": "hi-IN",
  "category": "crop_info",
  "question": "Which wheat variety is best for my region?"
}
```

#### Parameters

- **language**: Language code for the response (e.g., "hi-IN", "en-US", "pa-IN")
- **category**: Type of agricultural information needed
- **question**: The farmer's question or query

#### Supported Languages

- `en-US` - English
- `hi-IN` - Hindi
- `pa-IN` - Punjabi
- `bn-IN` - Bengali
- `ta-IN` - Tamil
- `te-IN` - Telugu
- `mr-IN` - Marathi
- `gu-IN` - Gujarati
- `kn-IN` - Kannada
- `ml-IN` - Malayalam

#### Supported Categories

- `weather_info` or `weather` - Weather Agent
- `crop_info` or `crop` or `crop_science` - Crop Science Agent
- `market_info` or `market` - Market Agent
- `finance_info` or `finance` - Finance Agent
- `soil_info` or `soil` or `soil_health` - Soil Health Agent

### Example API Calls

#### Weather Information in Hindi

```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "hi-IN",
    "category": "weather_info",
    "question": "पंजाब में इस सप्ताह गेहूं की खेती के लिए मौसम का पूर्वानुमान क्या है?"
  }'
```

#### Crop Advice in English

```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "en-US",
    "category": "crop_info",
    "question": "Which wheat variety is best for my region's soil type?"
  }'
```

#### Market Information in Punjabi

```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "pa-IN",
    "category": "market_info",
    "question": "ਮੇਰੇ ਖੇਤਰ ਵਿੱਚ ਕਣਕ ਦੇ ਵਰਤਮਾਨ ਮੁੱਲ ਕੀ ਹਨ?"
  }'
```

### Additional Endpoints

#### Get Available Categories

```bash
curl "http://localhost:8000/agents/categories"
```

Response:

```json
{
  "available_categories": [
    "weather_info",
    "crop_info",
    "market_info",
    "finance_info",
    "soil_info"
  ],
  "descriptions": {
    "weather_info": "Provides weather-related agricultural advice, forecasts, and climate information",
    "crop_info": "Offers crop selection, management, and science-based farming advice",
    "market_info": "Provides market prices, trends, and selling strategies for agricultural products",
    "finance_info": "Offers financial advice including loans, subsidies, and investment planning",
    "soil_info": "Provides soil health management, testing, and improvement recommendations"
  }
}
```

#### Legacy Endpoint (Backward Compatibility)

```bash
curl -X POST "http://localhost:8000/chat/stream/legacy" \
  -F "message=What crops grow well in my region?" \
  -F "namespace=optional_namespace"
```

## Agent Specializations

### Weather Agent

- **Expertise**: Weather forecasts, climate impact on farming, seasonal patterns
- **Tools Used**: Web search for current weather, knowledge base for historical patterns
- **Best For**: Planning farming activities, irrigation scheduling, weather-based decisions

### Crop Science Agent

- **Expertise**: Crop selection, pest management, growth stages, organic farming
- **Tools Used**: Knowledge base for best practices, web search for current research
- **Best For**: Crop planning, disease management, yield optimization

### Market Agent

- **Expertise**: Market prices, trends, selling strategies, supply-demand analysis
- **Tools Used**: Web search for current prices, knowledge base for market analysis
- **Best For**: Timing crop sales, understanding market dynamics, profit maximization

### Finance Agent

- **Expertise**: Loans, subsidies, insurance, investment planning, financial risk
- **Tools Used**: Web search for current programs, knowledge base for financial planning
- **Best For**: Financial planning, accessing government support, investment decisions

### Soil Health Agent

- **Expertise**: Soil testing, fertility management, organic amendments, erosion control
- **Tools Used**: Knowledge base for soil science, web search for current techniques
- **Best For**: Soil improvement, sustainable farming, long-term land health

## Implementation Details

### Adding New Agents

To add a new agent:

1. Create a new directory under `app/agents/`
2. Create `agent.py` with a class inheriting from `BaseAgent`
3. Override `_get_agent_specific_prompt()` method
4. Create `prompt.py` with language-specific prompts
5. Add the agent to `AgentFactory.AGENT_MAP`
6. Update this documentation

### Customizing Prompts

Each agent has a `prompt.py` file containing:

- System prompts in multiple languages
- Example questions for each specialization
- Language-specific instructions

### Tool Integration

All agents automatically have access to:

- Knowledge base search (Milvus vector database)
- Web search (DuckDuckGo API)
- Language-specific system instructions

## Dependencies

The system requires:

- `requests` for web search functionality
- `llama_index` for the agent framework
- `fastapi` for the API endpoints
- `pydantic` for request validation

## Future Enhancements

- Add more language support
- Implement agent-specific tools
- Add conversation memory
- Support for multi-agent conversations
- Integration with external agricultural APIs
- Mobile app support
- Voice interface capabilities
