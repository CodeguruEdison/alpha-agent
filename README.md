# ⬡ AlphaAgent

> Autonomous stock research platform powered entirely by open-source AI


---

## What is AlphaAgent?

AlphaAgent deploys a team of 7 specialized AI agents to analyze any
publicly traded stock. Each agent has a focused role — fetching market
data, scoring news sentiment, reading SEC filings, identifying chart
patterns, computing risk metrics — and a Strategy Agent synthesizes
all findings into a unified BUY / HOLD / SELL signal with price targets
and a full investment thesis.

Everything runs on open-source models via Ollama locally,
with Groq as a fast cloud fallback. Zero OpenAI dependency.

---

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Frontend       | Next.js 16, Tailwind CSS, Recharts|
| Backend        | FastAPI, LangGraph, Python 3.11   |
| Local LLMs     | Ollama (mistral, llama3, mixtral) |
| Cloud LLMs     | Groq API (free fallback)          |
| Sentiment      | FinBERT (HuggingFace)             |
| Vector DB      | ChromaDB (SEC filing RAG)         |
| Cache          | Redis                             |
| Database       | PostgreSQL via Supabase           |
| Auth           | NextAuth.js + Google OAuth        |
| Deployment     | Vercel (frontend) + Railway (backend) |

---

## AI Agents

| Agent          | Model          | Role                              |
|----------------|----------------|-----------------------------------|
| Market Data    | llama3.1:8b    | OHLCV + technical indicators      |
| Sentiment      | FinBERT        | News headline scoring             |
| Fundamental    | mixtral:8x7b   | P/E, EPS, SEC filing RAG          |
| Technical      | codellama:7b   | Chart patterns + signals          |
| Risk           | mistral:7b     | VaR, Sharpe, Beta                 |
| Strategy       | mixtral:8x7b   | BUY / HOLD / SELL synthesis       |
| Report         | mixtral:8x7b   | Investment thesis generation      |

---

## Quick Start

### Prerequisites
- Node.js LTS/Krypton (v20)
- Python 3.11+
- Docker + Docker Compose
- [Ollama](https://ollama.ai)

### 1. Clone and setup
```bash
git clone https://github.com/your-username/alphaagent.git
cd alphaagent
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Pull AI models
```bash
ollama pull mistral:7b
ollama pull llama3.1:8b
ollama pull mixtral:8x7b
ollama pull codellama:7b
```

### 3. Start all services
```bash
docker-compose up --build
```

### 4. Start frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Open the app
| Service     | URL                          |
|-------------|------------------------------|
| Frontend    | http://localhost:3000        |
| Backend API | http://localhost:8000        |
| API Docs    | http://localhost:8000/docs   |
| ChromaDB    | http://localhost:8001        |

---

## Project Structure
```
alphaagent/
├── frontend/               # Next.js 14 app
│   ├── app/                # App Router pages
│   ├── components/         # UI components
│   ├── hooks/              # Custom React hooks
│   └── lib/                # Utilities
├── backend/
│   ├── agents/             # 7 AI agents
│   ├── services/           # Market data, SEC, FRED
│   ├── tools/              # LangChain tools
│   ├── models/             # LLM config & router
│   ├── graph/              # LangGraph workflow
│   └── tests/              # pytest test suite
├── docker-compose.yml
└── .github/
    └── workflows/          # CI/CD pipelines
```

---

## API Keys Required

All free tiers — no credit card needed:

| Service        | Used For               | Link                              |
|----------------|------------------------|-----------------------------------|
| Groq           | LLM inference fallback | https://console.groq.com          |
| Polygon.io     | Real-time market data  | https://polygon.io                |
| Finnhub        | News + earnings        | https://finnhub.io                |
| Alpha Vantage  | Quotes + forex         | https://alphavantage.co           |
| FRED           | Macro indicators       | https://fred.stlouisfed.org       |

---

## Development
```bash
# Run backend tests
cd backend && uv run pytest tests/ -v

# Format code
cd backend && uv run black .

# Check types (frontend)
cd frontend && npx tsc --noEmit
```

---

## License

MIT
