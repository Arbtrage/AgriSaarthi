# Agrisathi RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system built with modern technologies for agricultural knowledge management and intelligent document processing.

## 🚀 Features

- **Intelligent Document Processing**: Multi-format document ingestion with smart chunking
- **Advanced Vector Search**: Direct Milvus integration with optimized similarity search
- **Real-time Chat Interface**: Streaming responses via Server-Sent Events (SSE)
- **Multi-tenant Support**: Namespace-based document isolation
- **Modern AI Integration**: Google Gemini for LLM and embeddings
- **Scalable Architecture**: Async operations with high-performance vector database

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Vector Store  │
│   (React/Next)  │◄──►│   (FastAPI)     │◄──►│   (Milvus)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   AI Services   │
                       │  (Google Gemini)│
                       └─────────────────┘
```

## 📋 Prerequisites

- **Python**: 3.13+
- **Node.js**: 18+ (for frontend)
- **Package Manager**: `uv` for Python, `npm` or `yarn` for Node.js
- **Vector Database**: Zilliz Cloud or Milvus instance
- **AI Services**: Google AI Studio API key

## 🛠️ Backend Implementation

### Environment Setup

Create a `.env` file in the server directory:

```bash
# AI Services
GOOGLE_API_KEY=your-google-api-key
GEMINI_MODEL=gemini-2.0-flash
EMBED_MODEL_NAME=text-embedding-004

# Vector Database
MILVUS_URI=grpc://your-zilliz-endpoint:19530
MILVUS_TOKEN=your_zilliz_api_key_or_user:pass
MILVUS_COLLECTION=rag_documents

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### Installation

```bash
# Navigate to server directory
cd server

# Install Python dependencies
uv sync

# Create Milvus collection
uv run python scripts/create_milvus_collection.py
```

### Running the Backend

```bash
# Development mode
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

#### Document Ingestion

```http
POST /ingest
Content-Type: multipart/form-data

Fields:
- files: One or more document files
- namespace: Optional project identifier
```

**Example:**

```bash
curl -X POST http://localhost:8000/ingest \
  -F "files=@/path/to/document.pdf" \
  -F "files=@/path/to/report.txt" \
  -F "namespace=agriculture-2024"
```

#### Chat Interface

```http
POST /chat/stream
Content-Type: application/x-www-form-urlencoded

Fields:
- message: User query text
- namespace: Optional project identifier
```

**Example:**

```bash
curl -N -X POST http://localhost:8000/chat/stream \
  -F "message=What are the best irrigation practices?" \
  -F "namespace=agriculture-2024"
```

### Backend Architecture

- **FastAPI**: Modern, fast web framework with automatic API documentation
- **LlamaIndex**: Intelligent document processing and RAG orchestration
- **PyMilvus**: Direct vector database integration for optimal performance
- **Google Gemini**: State-of-the-art LLM and embedding models
- **Async Operations**: Non-blocking I/O for better scalability

## 🎨 Frontend Implementation

### Technology Stack

- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS for modern, responsive design
- **State Management**: Zustand for lightweight state management
- **HTTP Client**: Axios for API communication
- **UI Components**: Headless UI + Radix UI for accessible components
- **Build Tool**: Vite for fast development and optimized builds

### Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # Reusable UI components
│   │   ├── chat/         # Chat interface components
│   │   ├── upload/       # Document upload components
│   │   └── layout/       # Layout and navigation
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API service layer
│   ├── stores/           # State management
│   ├── types/            # TypeScript type definitions
│   └── utils/            # Utility functions
├── public/               # Static assets
├── package.json
└── vite.config.ts
```

### Installation & Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Start development server
npm run dev
# or
yarn dev
```

### Key Features

#### 1. Document Upload Interface

- Drag & drop file upload
- Multi-file selection
- Progress indicators
- File type validation
- Namespace management

#### 2. Chat Interface

- Real-time streaming responses
- Message history
- Context-aware conversations
- Markdown rendering
- Code syntax highlighting

#### 3. Document Management

- Document library view
- Search and filtering
- Metadata display
- Chunk visualization

### Environment Configuration

Create `.env.local` in the frontend directory:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Agrisathi RAG

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
```

### Building for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview

# Deploy to hosting service
npm run deploy
```

## 🔧 Development

### Backend Development

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Code formatting
uv run black .
uv run isort .

# Linting
uv run flake8 .
uv run mypy .
```

### Frontend Development

```bash
# Install development dependencies
npm install --save-dev

# Run tests
npm run test

# Code formatting
npm run format

# Linting
npm run lint

# Type checking
npm run type-check
```

### Database Schema

The Milvus collection uses a simplified schema for optimal performance:

```python
{
    "embedding": Vector,      # 768-dimensional vector from Google GenAI
    "text": String,          # Document chunk text content
    "metadata": JSON {        # Structured metadata
        "source": String,     # Original filename
        "chunk_id": String,   # Unique chunk identifier
        "namespace": String,  # Project/tenant identifier
        "file_size": Integer, # Original file size in bytes
        "chunk_size": Integer,# Chunk size in characters
        "total_chunks": Integer # Total chunks in document
    }
}
```

## 🚀 Deployment

### Backend Deployment

#### Docker Deployment

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Environment Variables for Production

```bash
# Production settings
DEBUG=false
LOG_LEVEL=info
CORS_ORIGINS=https://yourdomain.com
```

### Frontend Deployment

#### Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

#### Netlify Deployment

```bash
# Build and deploy
npm run build
netlify deploy --prod --dir=dist
```

## 📊 Performance & Monitoring

### Backend Metrics

- Request/response times
- Vector search latency
- Memory usage
- Database connection pool status

### Frontend Metrics

- Page load times
- Bundle size analysis
- User interaction tracking
- Error monitoring

## 🔒 Security Considerations

- **API Authentication**: Implement JWT or OAuth2 for production
- **CORS Configuration**: Restrict origins in production
- **Rate Limiting**: Implement request throttling
- **Input Validation**: Sanitize all user inputs
- **HTTPS**: Use SSL/TLS in production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/TypeScript
- Write comprehensive tests
- Update documentation for new features
- Use conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LlamaIndex](https://github.com/run-llama/llama_index) for RAG orchestration
- [Milvus](https://milvus.io/) for vector database
- [Google Gemini](https://ai.google.dev/) for AI models
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [React](https://react.dev/) for the frontend framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/agrisathi/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/agrisathi/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/agrisathi/wiki)

---

**Built with ❤️ for the agricultural community**
