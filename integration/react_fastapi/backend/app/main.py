"""
FastAPI Backend for AI Research Assistant.

This module provides:
- POST /chat endpoint for sending messages
- Server-Sent Events (SSE) for streaming responses
- CORS configuration for frontend communication
"""

import json
from dotenv import load_dotenv

# Load environment variables FIRST (before other imports that need them)
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from langchain_core.messages import HumanMessage

from app.agent import agent


# Initialize FastAPI app
app = FastAPI(
    title="AI Research Assistant API",
    description="Backend API for the AI Research Assistant with streaming support",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model for chat endpoint
class ChatRequest(BaseModel):
    """Schema for incoming chat messages."""
    message: str


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - shows API is running."""
    return {"message": "AI Research Assistant API is running!", "docs": "/docs"}


# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy"}


# Chat endpoint with SSE streaming
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Process a chat message and stream the response.

    Args:
        request: ChatRequest containing the user's message

    Returns:
        EventSourceResponse with streaming AI response
    """

    async def generate():
        """Generator function that yields SSE events."""
        try:
            # Create the input message for the agent
            input_messages = {"messages": [HumanMessage(content=request.message)]}

            # Use astream for streaming (each chunk is already just the new token)
            async for chunk in agent.astream(input_messages, stream_mode="messages"):
                # chunk is a tuple: (AIMessageChunk, metadata)
                if isinstance(chunk, tuple) and len(chunk) >= 1:
                    message = chunk[0]
                    # Only stream AI message content (not tool calls)
                    if hasattr(message, "content") and message.content:
                        # Skip if it's a tool call
                        if hasattr(message, "tool_calls") and message.tool_calls:
                            continue
                        # Send the token directly (it's already just the new content)
                        yield {
                            "event": "token",
                            "data": json.dumps({"content": message.content})
                        }

            # Signal that streaming is complete
            yield {
                "event": "done",
                "data": json.dumps({"status": "complete"})
            }

        except Exception as e:
            # Send error to frontend
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }

    # Return the streaming response
    return EventSourceResponse(generate())


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
