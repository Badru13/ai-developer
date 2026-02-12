"""
Test script to debug streaming behavior.
Run with: python test_stream.py
"""

import asyncio
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from app.agent import agent


async def test_streaming():
    """Test the agent streaming to see exact output structure."""

    input_messages = {"messages": [HumanMessage(content="hi")]}

    print("=" * 50)
    print("Testing stream_mode='messages'")
    print("=" * 50)

    async for chunk in agent.astream(input_messages, stream_mode="messages"):
        print(f"\nChunk type: {type(chunk)}")
        print(f"Chunk: {chunk}")
        if isinstance(chunk, tuple):
            print(f"  Tuple length: {len(chunk)}")
            for i, item in enumerate(chunk):
                print(f"  Item {i}: {type(item)} = {item}")

    print("\n" + "=" * 50)
    print("Testing astream_events")
    print("=" * 50)

    input_messages2 = {"messages": [HumanMessage(content="hi")]}

    async for event in agent.astream_events(input_messages2, version="v2"):
        event_type = event.get("event")
        if event_type == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            name = event.get("name", "")
            tags = event.get("tags", [])
            parent_ids = event.get("parent_ids", [])
            print(f"\nEvent: {event_type}")
            print(f"  Name: {name}")
            print(f"  Tags: {tags}")
            print(f"  Parent IDs count: {len(parent_ids)}")
            if chunk:
                print(f"  Chunk content: '{chunk.content}'")


if __name__ == "__main__":
    asyncio.run(test_streaming())
