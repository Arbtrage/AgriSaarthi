# Tavily Web Search Integration

This document explains how to set up and use Tavily web search in the AgriSaarthi project.

## What is Tavily?

Tavily is an AI-native search engine that provides high-quality, real-time web search results. It's particularly useful for:

- Getting current agricultural market information
- Finding latest farming technology trends
- Accessing real-time weather data
- Researching crop diseases and treatments
- Finding market prices and demand information

## Setup Instructions

### 1. Get a Tavily API Key

1. Visit [Tavily's website](https://tavily.com/)
2. Sign up for an account
3. Navigate to your dashboard to get your API key
4. Copy the API key

### 2. Configure Environment Variables

Add the following to your `.env` file:

```bash
TAVILY_API_KEY=your_tavily_api_key_here
```

Or export it in your shell:

```bash
export TAVILY_API_KEY="your_tavily_api_key_here"
```

### 3. Install Dependencies

The project now includes the `tavily-python` package. Install it with:

```bash
uv sync
```

Or if you're using pip:

```bash
pip install tavily-python
```

## Usage

### In Agent Tools

The web search tool is automatically available to all agents and can be used with:

```python
from app.agents.tools import build_web_search_tool

web_search_tool = build_web_search_tool()
result = await web_search_tool.fn(
    query="latest wheat prices in India",
    search_depth="basic",  # or "advanced"
    max_results=5
)
```

### Parameters

- **query** (str): The search query
- **search_depth** (str): Either "basic" (faster) or "advanced" (more comprehensive)
- **max_results** (int): Maximum number of results to return (default: 5)

### Example Queries

Here are some example queries that work well with agricultural contexts:

- "current rice market prices Asia 2024"
- "latest agricultural drone technology innovations"
- "soil health monitoring best practices 2024"
- "climate change impact on wheat production"
- "organic farming certification requirements India"
- "agricultural subsidies government programs 2024"

## Testing

Run the test script to verify your setup:

```bash
python test_tavily.py
```

## Features

### Smart Answer Generation

Tavily can provide direct answers to questions when available, making it easier to get quick insights.

### Source Attribution

All results include source URLs, allowing users to verify information and access original content.

### Agricultural Context

The tool is optimized for agricultural queries and can handle technical farming terminology.

### Real-time Information

Get the most current information about markets, weather, and agricultural developments.

## Error Handling

The tool includes comprehensive error handling for:

- Missing API keys
- Network issues
- API rate limits
- Invalid queries

## Cost Considerations

- Tavily offers a free tier with limited searches
- Paid plans provide higher limits and advanced features
- Monitor your usage in the Tavily dashboard

## Troubleshooting

### Common Issues

1. **API Key Not Found**

   - Ensure `TAVILY_API_KEY` is set in your environment
   - Check that the `.env` file is loaded

2. **Rate Limiting**

   - Tavily has rate limits on free accounts
   - Consider upgrading for higher usage

3. **Search Failures**
   - Check your internet connection
   - Verify the query format
   - Check Tavily service status

### Getting Help

- Check [Tavily's documentation](https://docs.tavily.com/)
- Review the error messages in the tool output
- Ensure your API key is valid and active

## Integration with Agents

The web search tool is integrated with the agent system and can be used by:

- Crop Science Agent
- Market Agent
- Weather Agent
- Finance Agent
- Soil Health Agent

Each agent can leverage web search to provide up-to-date information and enhance their responses with current data.
