"""
Conversation memory management for LangChain.

Provides factory functions for creating memory instances and
utilities for persisting / loading conversation history to JSON files.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Optional

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

# Default directory for saved conversations
CONVERSATIONS_DIR: str = "data/conversations"


def get_conversation_memory() -> ConversationBufferMemory:
    """
    Initializes and returns a ConversationBufferMemory instance.

    Returns:
        A fresh LangChain conversation memory.
    """
    print("Initializing conversation memory (ConversationBufferMemory).")
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def save_conversation(memory: ConversationBufferMemory, filepath: Optional[str] = None) -> str:
    """
    Saves the current conversation history to a JSON file.

    Args:
        memory: The conversation memory to persist.
        filepath: Optional custom path. Defaults to a timestamped file
                  inside ``data/conversations/``.

    Returns:
        The path to the saved JSON file.
    """
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    if filepath is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(CONVERSATIONS_DIR, f"conversation_{timestamp}.json")

    history: dict[str, Any] = memory.load_memory_variables({})
    messages: list[BaseMessage] = history.get("chat_history", [])

    serialized: list[dict[str, str]] = []
    for msg in messages:
        serialized.append({"role": msg.type, "content": msg.content})

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            {"saved_at": datetime.now(timezone.utc).isoformat(), "messages": serialized},
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Conversation saved to {filepath} ({len(serialized)} messages).")
    return filepath


def load_conversation(filepath: str, memory: Optional[ConversationBufferMemory] = None) -> ConversationBufferMemory:
    """
    Loads a conversation from a JSON file into a memory instance.

    Args:
        filepath: Path to the JSON conversation file.
        memory: Optional existing memory to load into.
                If ``None``, a new memory instance is created.

    Returns:
        The memory instance populated with the loaded conversation.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Conversation file not found: {filepath}")

    if memory is None:
        memory = get_conversation_memory()

    with open(filepath, "r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)

    messages: list[dict[str, str]] = data.get("messages", [])

    # Replay messages pairwise (human, ai) into memory
    i = 0
    while i < len(messages) - 1:
        human_msg = messages[i]
        ai_msg = messages[i + 1]
        if human_msg["role"] == "human" and ai_msg["role"] == "ai":
            memory.save_context({"input": human_msg["content"]}, {"output": ai_msg["content"]})
            i += 2
        else:
            i += 1

    print(f"Loaded conversation from {filepath} ({len(messages)} messages).")
    return memory


def list_saved_conversations() -> list[str]:
    """
    Returns a list of saved conversation file paths, sorted newest first.
    """
    if not os.path.exists(CONVERSATIONS_DIR):
        return []
    files = [
        os.path.join(CONVERSATIONS_DIR, f)
        for f in os.listdir(CONVERSATIONS_DIR)
        if f.endswith(".json")
    ]
    files.sort(key=os.path.getmtime, reverse=True)
    return files


# Example usage
if __name__ == "__main__":
    print("--- Running Memory Example ---")
    mem = get_conversation_memory()

    mem.save_context({"input": "Hi there!"}, {"output": "Hello! How can I help you today?"})
    mem.save_context({"input": "What's the weather like?"}, {"output": "I'm sorry, I don't have real-time weather access."})

    saved_path = save_conversation(mem)

    loaded_mem = load_conversation(saved_path)
    history = loaded_mem.load_memory_variables({})
    print("\nLoaded conversation:")
    for message in history["chat_history"]:
        print(f"- {message.type.capitalize()}: {message.content}")

    print(f"\nSaved conversations: {list_saved_conversations()}")
    print("\n--- Memory Example Finished ---")
