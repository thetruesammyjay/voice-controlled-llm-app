import os 
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

# Import specific components from sibling modules
from src.llm.prompts import get_default_prompt
from src.llm.memory import get_conversation_memory
from src.utils.config import config # Assuming config is accessible here

def get_conversation_chain(llm: ChatOpenAI = None,
                           memory: ConversationBufferMemory = None,
                           prompt_template: ChatPromptTemplate = None,
                           verbose: bool = False) -> ConversationChain:
    """
    Configures and returns a LangChain ConversationChain.

    Args:
        llm (ChatOpenAI, optional): The language model instance. If None, a default
                                   is created using config.
        memory (ConversationBufferMemory, optional): The memory instance. If None,
                                                    a default is created.
        prompt_template (ChatPromptTemplate, optional): The prompt template to use.
                                                        If None, a default is used.
        verbose (bool): If True, enables verbose logging for the chain.

    Returns:
        ConversationChain: A configured LangChain ConversationChain.
    """
    print("Configuring LangChain ConversationChain.")

    # Use provided instances or create defaults based on configuration
    if llm is None:
        llm = ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            openai_api_key=config.OPENAI_API_KEY
        )
        print(f"Default ChatOpenAI LLM created: {config.MODEL_NAME}")

    if memory is None:
        memory = get_conversation_memory()
        print("Default conversation memory initialized.")

    if prompt_template is None:
        prompt_template = get_default_prompt()
        print("Default prompt template loaded.")

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt_template,
        verbose=verbose
    )
    print("ConversationChain successfully created.")
    return chain

# Example usage
if __name__ == "__main__":
    print("--- Running Chains Example ---")
    # For this example, we'll need to set up a dummy OpenAI key for ChatOpenAI to initialize
    # In a real run, this would be handled by your .env and config.py
    if not hasattr(config, 'OPENAI_API_KEY') or not config.OPENAI_API_KEY:
        print("WARNING: OPENAI_API_KEY not set in config. Using dummy for example.")
        # This will still likely fail if OpenAI API key is truly missing and calls are made.
        # This is for internal testing of chain creation, not full functionality.
        os.environ["OPENAI_API_KEY"] = "dummy-key-for-testing"

    try:
        # Get a conversation chain with default settings
        my_chain = get_conversation_chain(verbose=True)
        print("\nChain initialized. Try predicting (will make an API call if key is valid):")
        # This will attempt an OpenAI API call
        # response = my_chain.predict(input="Hello, tell me a fun fact about Python.")
        # print(f"AI Response: {response}")

        # You can also pass specific LLM/memory/prompt instances
        from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
        from langchain.memory import ConversationBufferWindowMemory # Example of a different memory type

        custom_llm = ChatOpenAI(
            model="gpt-4o-mini", # Another model
            temperature=0.9,
            openai_api_key=config.OPENAI_API_KEY
        )
        custom_memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=2) # Keep last 2 exchanges
        custom_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("You are a poetic AI."),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        poetic_chain = get_conversation_chain(llm=custom_llm, memory=custom_memory, prompt_template=custom_prompt)
        print("\nPoetic chain initialized.")
        # response_poetic = poetic_chain.predict(input="Write a haiku about the moon.")
        # print(f"Poetic AI Response: {response_poetic}")

    except Exception as e:
        print(f"An error occurred during chain example (this might happen if OPENAI_API_KEY is invalid): {e}")

    print("\n--- Chains Example Finished ---")

