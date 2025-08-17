# 🌾 AgriSaarthi - AI-Powered Agricultural Assistant

AgriSaarthi is a comprehensive AI-powered agricultural assistance platform that provides farmers with expert advice on crops, fertilizers, market prices, government schemes, and more. The platform features a multi-agent system with support for multiple languages and both markdown and plain text responses.

## 🏗️ Architecture Overview

### Backend Architecture

```
AgriSaarthi/
├── app/
│   ├── agents/           # Multi-agent system for specialized agricultural advice
│   │   ├── base_agent.py # Base agent class with common functionality
│   │   ├── agent_factory.py # Factory for creating specialized agents
│   │   ├── crop_science_agent/    # Crop-related advice
│   │   ├── fertilizer_agent/      # Fertilizer recommendations
│   │   ├── market_agent/          # Market prices and trends
│   │   ├── gov_schemes_agent/     # Government schemes and subsidies
│   │   ├── weather_agent/         # Weather-related advice
│   │   ├── finance_agent/         # Financial planning
│   │   ├── soil_health_agent/     # Soil health management
│   │   └── other_agent/           # General agricultural advice
│   ├── api/              # FastAPI REST endpoints
│   │   └── routers/
│   │       ├── chat.py   # Chat endpoints with streaming support
│   │       └── ingest.py # Document ingestion endpoints
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration management
│   │   ├── llm.py        # LLM integration
│   │   ├── qdrant_client.py # Vector database client
│   │   └── vector_store.py # Vector store operations
│   ├── mcp/              # Model Context Protocol server
│   │   └── mcp.py        # MCP server for external integrations
│   └── utils/            # Utility functions
│       ├── chunking.py   # Document chunking utilities
│       └── parsing.py    # Document parsing utilities
├── web/                  # Next.js frontend application
│   ├── app/              # App router components
│   │   ├── components/   # React components
│   │   │   ├── ChatInterface.tsx # Main chat interface
│   │   │   └── HomeScreen.tsx    # Home screen component
│   │   ├── layout.tsx    # Root layout
│   │   └── page.tsx      # Main page
│   ├── tailwind.config.ts # Tailwind CSS configuration
│   └── package.json      # Frontend dependencies
├── tests/                # Test suite
├── main.py               # FastAPI application entry point
├── docker-compose.yml    # Docker orchestration
└── pyproject.toml        # Python project configuration
```

### Multi-Agent System

The platform uses a sophisticated multi-agent system where each agent specializes in a specific agricultural domain:

- **Crop Science Agent**: Crop selection, management, and best practices
- **Fertilizer Agent**: Fertilizer recommendations and application rates
- **Market Agent**: Market prices, trends, and selling strategies
- **Government Schemes Agent**: Subsidies, loans, and support programs
- **Weather Agent**: Weather forecasts and climate-based advice
- **Finance Agent**: Financial planning and loan options
- **Soil Health Agent**: Soil testing and improvement strategies
- **Other Agent**: General agricultural advice and tips

## 🚀 Features

### 🌍 Multi-Language Support

- **English (en-US/en-IN)**: Primary language with technical terminology
- **Hindi (hi-IN)**: Native language support for Indian farmers
- **Punjabi (pa-IN)**: Regional language support
- **Bengali (bn-IN)**: Eastern region language support
- **Tamil (ta-IN)**: Southern region language support
- **Telugu (te-IN)**: Andhra Pradesh/Telangana support
- **Marathi (mr-IN)**: Maharashtra region support
- **Gujarati (gu-IN)**: Gujarat region support
- **Kannada (kn-IN)**: Karnataka region support
- **Malayalam (ml-IN)**: Kerala region support

### 📝 Response Formatting

- **Markdown Mode**: Rich formatting with headers, lists, tables, and links
- **Plain Text Mode**: Clean text optimized for text-to-speech applications

### 🔍 Intelligent Search

- **Knowledge Base Search**: Vector-based search through agricultural documents
- **Web Search**: Real-time information from the internet
- **Confidence-Based Responses**: Agents never say "I don't know" - they provide confident, actionable advice

### 📱 Modern Web Interface

- **Next.js 14**: Modern React framework with App Router
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Works on all devices
- **Real-time Chat**: Streaming responses for better user experience

## 🛠️ Technology Stack

### Backend

- **FastAPI**: High-performance Python web framework
- **LlamaIndex**: LLM orchestration and RAG capabilities
- **Qdrant**: Vector database for semantic search
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI

### Frontend

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Hooks**: Modern React patterns

### AI/ML

- **Multi-Agent System**: Specialized agents for different domains
- **RAG (Retrieval Augmented Generation)**: Combines knowledge base with LLM capabilities
- **Vector Search**: Semantic similarity search
- **Streaming Responses**: Real-time AI responses

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose (optional)

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd AgriSaarthi
   ```

2. **Set up Python environment**

   ```bash
   # Create virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Environment configuration**

   ```bash
   # Copy environment template
   cp env.example .env

   # Edit .env with your configuration
   nano .env
   ```

4. **Run the backend**

   ```bash
   python main.py
   ```

   The FastAPI app will start on `http://localhost:8000`
   The MCP server will start on port `3005`

### Frontend Setup

1. **Navigate to web directory**

   ```bash
   cd web
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Run the development server**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### Docker Setup (Alternative)

1. **Start all services**

   ```bash
   docker-compose up -d
   ```

2. **Access services**
   - Backend API: `http://localhost:8000`
   - Frontend: `http://localhost:3000`
   - MCP Server: Port `3005`

## 📚 API Documentation

### Chat Endpoints

#### Stream Chat Response

```http
POST /chat/stream
Content-Type: application/json

{
  "language": "en-IN",
  "category": "crop_info",
  "question": "What are the best wheat varieties for my region?",
  "markdown": true
}
```

#### Complete Chat Response

```http
POST /chat
Content-Type: application/json

{
  "language": "hi-IN",
  "category": "fertilizers",
  "question": "मेरी गेहूं की फसल के लिए कौन सी खाद सबसे अच्छी है?",
  "markdown": false
}
```

### Agent Categories

```http
GET /agents/categories
```

Returns available agent categories and their descriptions.

### Health Check

```http
GET /health
```

Returns service health status.

## 🧪 Testing

Run the test suite to verify all components are working:

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python tests/test_markdown.py
python tests/test_agents.py
python tests/test_all_agents.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=agrisathi

# Web Search
TAVILY_API_KEY=your_tavily_api_key

# MCP Server
MCP_PORT=3005
```

### Agent Configuration

Each agent can be configured with:

- **Language**: Response language preference
- **Markdown**: Response formatting preference
- **Specialization**: Domain-specific knowledge and tools

## 🌐 MCP (Model Context Protocol) Integration

The platform includes an MCP server that allows external applications to integrate with the agricultural knowledge base:

- **Port**: 3005 (configurable)
- **Tools Available**:
  - `search_knowledgebase`: Search agricultural knowledge base
  - `web_search`: Search web for current information

### MCP Client Example

```python
from mcp import ClientSession, StdioServerParameters
import asyncio

async def main():
    async with ClientSession(StdioServerParameters(
        command="python", args=["-m", "app.mcp.mcp"]
    )) as session:
        # Search knowledge base
        result = await session.call_tool("search_knowledgebase", {"query": "wheat cultivation"})
        print(result.content)
```

## 📱 Frontend Features

### Chat Interface

- **Real-time Streaming**: Responses appear as they're generated
- **Language Selection**: Choose from 10 supported languages
- **Agent Selection**: Select specialized agricultural agents
- **Response Formatting**: Toggle between markdown and plain text
- **Mobile Responsive**: Works seamlessly on all devices

### User Experience

- **Intuitive Design**: Clean, farmer-friendly interface
- **Fast Response**: Optimized for quick agricultural advice
- **Accessibility**: Designed for users with varying technical skills

## 🔒 Security & Privacy

- **API Rate Limiting**: Prevents abuse and ensures fair usage
- **Input Validation**: All user inputs are validated and sanitized
- **Secure Communication**: HTTPS encryption for all communications
- **Data Privacy**: User data is not stored or logged

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions

## 🚀 Roadmap

- [ ] Voice input/output support
- [ ] Mobile app development
- [ ] Offline mode for basic queries
- [ ] Integration with IoT sensors
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant support for organizations

---

**Built with ❤️ for the farming community**

_AgriSaarthi - Empowering farmers with AI-driven agricultural intelligence_
