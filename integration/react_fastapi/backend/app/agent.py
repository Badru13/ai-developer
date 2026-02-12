"""
LangGraph Agent for the AI Research Assistant.

This module creates a ReAct-style agent that can:
- Answer questions using its knowledge
- Search the web for current information
- Get weather data for any city
- Perform calculations
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.tools import all_tools


# System prompt that defines the agent's behavior
SYSTEM_PROMPT = """You are a helpful AI Research Assistant. You can help users by:

1. Answering questions from your knowledge
2. Searching the web for current information (use search_web tool)
3. Getting weather for any city (use get_weather tool)
4. Doing math calculations (use calculator tool)

Guidelines:
- Be concise and helpful
- Use tools when you need current information or specific data
- Always cite sources when using search results
- If you're unsure, search for the information rather than guessing
"""


def create_agent():
    """
    Create and return the LangGraph agent.

    Returns:
        A compiled LangGraph agent ready to process messages
    """
    # Initialize the OpenAI LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Fast and cost-effective
        temperature=0.7,
        streaming=True  # Enable streaming for real-time responses
    )

    # Create the ReAct agent with tools
    agent = create_react_agent(
        model=llm,
        tools=all_tools,
        prompt=SYSTEM_PROMPT  # Add our system prompt
    )

    return agent


# Create a single agent instance to reuse
agent = create_agent()
