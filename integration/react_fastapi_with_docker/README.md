# AI Research Assistant

A full-stack application demonstrating **React + Tailwind**, **FastAPI**, and **LangGraph** working together.

## What This App Does

A chat interface where you can:
- Ask questions and get AI-powered responses
- Search the web for current information
- Get weather for any city
- Perform calculations

The AI agent decides which tools to use based on your question.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Tailwind CSS, Vite |
| Backend | FastAPI, Server-Sent Events (SSE) |
| AI Agent | LangGraph, LangChain, OpenAI |

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py      # FastAPI server with SSE streaming
│   │   ├── agent.py     # LangGraph agent setup
│   │   └── tools.py     # Web search, weather, calculator
│   ├── .env.example     # Environment variables template
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   └── InputBox.jsx
│   │   ├── App.jsx      # Main app with streaming logic
│   │   └── main.jsx
│   └── package.json
│
└── README.md
```

---

## Setup Instructions

### Step 1: Get API Keys (Free Tiers Available)

1. **OpenAI API Key**
   - Go to https://platform.openai.com/api-keys
   - Create an account and generate an API key

2. **Tavily API Key** (for web search)
   - Go to https://tavily.com
   - Sign up for free (1000 searches/month)

3. **OpenWeather API Key** (for weather)
   - Go to https://openweathermap.org/api
   - Sign up for free (1000 calls/day)

---

### Step 2: Setup Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# TAVILY_API_KEY=tvly-...
# OPENWEATHER_API_KEY=...

# Start the server
uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000

---

### Step 3: Setup Frontend

```bash
# Open a new terminal
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: http://localhost:5173

---

## How to Use

1. Open http://localhost:5173 in your browser
2. Type a message in the input box
3. Try these example prompts:

**Web Search:**
> "What are the latest news about AI?"

**Weather:**
> "What's the weather in Tokyo?"

**Calculator:**
> "Calculate 15% tip on $85"

**General Questions:**
> "Explain how solar panels work"

---

## Key Learning Concepts

### React + Tailwind
- Component-based architecture
- useState for state management
- useEffect for side effects
- Tailwind utility classes for styling

### FastAPI
- REST API endpoints
- Pydantic models for validation
- SSE (Server-Sent Events) for streaming
- CORS middleware configuration

### LangGraph
- Creating a ReAct agent
- Defining tools with `@tool` decorator
- Streaming agent responses
- Handling tool calls in the agent loop

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat` | Send message, receive SSE stream |

---

## Troubleshooting

**CORS Error:**
Make sure the backend is running on port 8000

**API Key Errors:**
Check that your `.env` file has valid API keys

**Module Not Found:**
Make sure you activated the virtual environment

---

## Next Steps for Students

1. Add more tools (e.g., stock prices, news API)
2. Add chat history persistence (database)
3. Add user authentication
4. Deploy to cloud (Vercel + Railway)
