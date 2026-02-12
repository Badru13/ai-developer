"""
Tools for the AI Research Assistant Agent.

This module defines three tools:
1. search_web - Search the internet using Tavily API
2. get_weather - Get current weather using OpenWeather API
3. calculator - Perform mathematical calculations
"""

import os
import httpx
import numexpr
from langchain_core.tools import tool
from tavily import TavilyClient


# Initialize Tavily client for web search
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


import re

def clean_search_content(text: str) -> str:
    """Remove markdown symbols and clean up scraped web content."""
    # Remove markdown headers
    text = re.sub(r'#{1,6}\s*', '', text)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


@tool
def search_web(query: str) -> str:
    """
    Search the web for information on any topic.
    Use this when you need to find current information, facts, or research a topic.

    Args:
        query: The search query string

    Returns:
        Search results with relevant information
    """
    try:
        # Perform search with Tavily
        response = tavily_client.search(
            query=query,
            max_results=3,
            search_depth="basic"
        )

        # Format results cleanly for the agent
        results = []
        for i, item in enumerate(response.get("results", []), 1):
            title = item.get("title", "No title")
            content = clean_search_content(item.get("content", "No content"))
            url = item.get("url", "")
            results.append(f"{i}. {title}\n   {content}\n   Source: {url}")

        return "\n\n".join(results) if results else "No results found."

    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city.
    Use this when the user asks about weather conditions.

    Args:
        city: The name of the city (e.g., "London", "New York")

    Returns:
        Current weather information for the city
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather"

        # Make API request
        with httpx.Client() as client:
            response = client.get(
                url,
                params={
                    "q": city,
                    "appid": api_key,
                    "units": "metric"  # Celsius
                }
            )
            response.raise_for_status()
            data = response.json()

        # Extract weather info
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        city_name = data["name"]
        country = data["sys"]["country"]

        return (
            f"Weather in {city_name}, {country}:\n"
            f"- Condition: {weather.capitalize()}\n"
            f"- Temperature: {temp}°C\n"
            f"- Feels like: {feels_like}°C\n"
            f"- Humidity: {humidity}%"
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling."
        return f"Weather API error: {str(e)}"
    except Exception as e:
        return f"Error getting weather: {str(e)}"


@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    Use this for any math operations like addition, multiplication, percentages, etc.

    Args:
        expression: A mathematical expression (e.g., "25 * 4 + 10", "100 / 5")

    Returns:
        The calculated result
    """
    try:
        # Safely evaluate the mathematical expression
        result = numexpr.evaluate(expression).item()
        return f"Result: {expression} = {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}. Please use valid math expressions."


# List of all tools for the agent
all_tools = [search_web, get_weather, calculator]
