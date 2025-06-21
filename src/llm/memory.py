from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage # Used for type hinting if needed

def get_conversation_memory() -> ConversationBufferMemory:
    """
    Initializes and returns a ConversationBufferMemory instance for LangChain.
    This memory stores the entire conversation history in a buffer.

    Returns:
        ConversationBufferMemory: An instance of LangChain's conversation memory.
    """
    print("Initializing conversation memory (ConversationBufferMemory).")
    # memory_key should match the variable_name in MessagesPlaceholder in your prompt
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Example usage
if __name__ == "__main__":
    print("--- Running Memory Example ---")
    memory = get_conversation_memory()
    print(f"Memory type: {type(memory)}")

    # Add some messages to memory
    memory.save_context({"input": "Hi there!"}, {"output": "Hello! How can I help you today?"})
    memory.save_context({"input": "What's the weather like?"}, {"output": "I'm sorry, I don't have real-time weather access."})

    # Load messages from memory
    history = memory.load_memory_variables({})
    print("\nConversation History:")
    for message in history["chat_history"]:
        print(f"- {message.type.capitalize()}: {message.content}")

    # Clear memory
    memory.clear()
    print("\nMemory cleared. History after clearing:")
    print(memory.load_memory_variables({}))
    print("\n--- Memory Example Finished ---")
