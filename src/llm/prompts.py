from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate

def get_default_prompt() -> ChatPromptTemplate:
    """
    Returns a default conversation prompt template, including chat history.
    """
    print("Loading default prompt template.")
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a helpful and friendly AI assistant. Keep your responses concise and relevant."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

def get_creative_prompt() -> ChatPromptTemplate:
    """
    Returns a prompt template designed for more creative and imaginative responses.
    """
    print("Loading creative prompt template.")
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a highly creative and imaginative AI assistant. "
            "Feel free to invent scenarios, tell stories, or offer unique perspectives. "
            "Be whimsical and engaging."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

def get_technical_prompt() -> ChatPromptTemplate:
    """
    Returns a prompt template optimized for technical discussions and factual accuracy.
    """
    print("Loading technical prompt template.")
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a precise and knowledgeable technical AI assistant. "
            "Focus on providing accurate, detailed, and factual information. "
            "Avoid speculation and clearly state when information is beyond your current knowledge."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

# Example usage
if __name__ == "__main__":
    print("--- Running Prompt Examples ---")
    default_prompt = get_default_prompt()
    creative_prompt = get_creative_prompt()
    technical_prompt = get_technical_prompt()

    # You can inspect the prompt structure (though not directly "run" without an LLM)
    print("\nDefault Prompt Messages:")
    for msg_template in default_prompt.messages:
        print(f"- {msg_template.input_variables}, {msg_template.lc_attributes}")

    print("\nCreative Prompt Messages:")
    for msg_template in creative_prompt.messages:
        print(f"- {msg_template.input_variables}, {msg_template.lc_attributes}")

    print("\nTechnical Prompt Messages:")
    for msg_template in technical_prompt.messages:
        print(f"- {msg_template.input_variables}, {msg_template.lc_attributes}")
    print("\n--- Prompt Examples Finished ---")
