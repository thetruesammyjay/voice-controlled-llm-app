"""
Tests for the LLM module (chains, prompts, memory).
Uses mocking to avoid requiring an OpenAI API key.
"""

import os

# Set dummy API key BEFORE importing src modules
os.environ.setdefault("OPENAI_API_KEY", "test-key-for-testing")

import pytest
from unittest.mock import patch, MagicMock

from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory

from src.llm.memory import get_conversation_memory
from src.llm.prompts import get_default_prompt, get_creative_prompt, get_technical_prompt
from src.llm.chains import get_conversation_chain


# ═══════════════════════════════════════════════════
# Memory Tests
# ═══════════════════════════════════════════════════

class TestConversationMemory:
    """Tests for conversation memory management."""

    def test_get_conversation_memory_returns_buffer(self):
        """Test that get_conversation_memory returns a ConversationBufferMemory."""
        memory = get_conversation_memory()
        assert isinstance(memory, ConversationBufferMemory)

    def test_memory_key_is_chat_history(self):
        """Test memory key matches the prompt placeholder."""
        memory = get_conversation_memory()
        assert memory.memory_key == "chat_history"

    def test_memory_returns_messages(self):
        """Test memory is configured to return message objects."""
        memory = get_conversation_memory()
        assert memory.return_messages is True

    def test_memory_save_and_load(self):
        """Test saving and loading context from memory."""
        memory = get_conversation_memory()

        memory.save_context(
            {"input": "Hello"},
            {"output": "Hi there!"}
        )

        history = memory.load_memory_variables({})
        assert "chat_history" in history
        assert len(history["chat_history"]) == 2  # One HumanMessage + one AIMessage

    def test_memory_clear(self):
        """Test clearing memory removes all messages."""
        memory = get_conversation_memory()

        memory.save_context(
            {"input": "Hello"},
            {"output": "Hi!"}
        )
        memory.clear()

        history = memory.load_memory_variables({})
        assert len(history["chat_history"]) == 0

    def test_memory_multiple_exchanges(self):
        """Test memory stores multiple conversation exchanges."""
        memory = get_conversation_memory()

        memory.save_context({"input": "First"}, {"output": "Response 1"})
        memory.save_context({"input": "Second"}, {"output": "Response 2"})
        memory.save_context({"input": "Third"}, {"output": "Response 3"})

        history = memory.load_memory_variables({})
        assert len(history["chat_history"]) == 6  # 3 pairs


# ═══════════════════════════════════════════════════
# Prompt Tests
# ═══════════════════════════════════════════════════

class TestPrompts:
    """Tests for prompt template functions."""

    def test_get_default_prompt_returns_template(self):
        """Test default prompt returns a ChatPromptTemplate."""
        prompt = get_default_prompt()
        assert isinstance(prompt, ChatPromptTemplate)

    def test_get_default_prompt_has_messages(self):
        """Test default prompt has system, history, and human messages."""
        prompt = get_default_prompt()
        assert len(prompt.messages) == 3  # System + History + Human

    def test_get_creative_prompt_returns_template(self):
        """Test creative prompt returns a ChatPromptTemplate."""
        prompt = get_creative_prompt()
        assert isinstance(prompt, ChatPromptTemplate)

    def test_get_creative_prompt_has_messages(self):
        """Test creative prompt has correct number of messages."""
        prompt = get_creative_prompt()
        assert len(prompt.messages) == 3

    def test_get_technical_prompt_returns_template(self):
        """Test technical prompt returns a ChatPromptTemplate."""
        prompt = get_technical_prompt()
        assert isinstance(prompt, ChatPromptTemplate)

    def test_get_technical_prompt_has_messages(self):
        """Test technical prompt has correct number of messages."""
        prompt = get_technical_prompt()
        assert len(prompt.messages) == 3

    def test_default_prompt_has_input_variable(self):
        """Test default prompt accepts 'input' variable."""
        prompt = get_default_prompt()
        # The human message template should contain {input}
        human_msg = prompt.messages[-1]
        assert "input" in human_msg.input_variables

    def test_all_prompts_are_distinct(self):
        """Test that all three prompts are different objects."""
        default = get_default_prompt()
        creative = get_creative_prompt()
        technical = get_technical_prompt()

        assert default is not creative
        assert default is not technical
        assert creative is not technical


# ═══════════════════════════════════════════════════
# Chains Tests
# ═══════════════════════════════════════════════════

from langchain_core.language_models.fake import FakeListLLM

class TestConversationChain:
    """Tests for conversation chain configuration."""

    @patch("src.llm.chains.config")
    @patch("src.llm.chains.ChatOpenAI")
    def test_get_conversation_chain_with_defaults(self, mock_llm_cls, mock_config):
        """Test chain creation with default parameters."""
        mock_config.MODEL_NAME = "gpt-3.5-turbo"
        mock_config.TEMPERATURE = 0.7
        mock_config.MAX_TOKENS = 150
        mock_config.OPENAI_API_KEY = "test-key"
        
        # Return a valid Langchain LLM to pass Pydantic validation
        mock_llm_cls.return_value = FakeListLLM(responses=["test"])

        chain = get_conversation_chain(verbose=False)

        assert chain is not None
        assert chain.memory is not None
        mock_llm_cls.assert_called_once()

    @patch("src.llm.chains.config")
    def test_get_conversation_chain_with_custom_llm(self, mock_config):
        """Test chain creation with a custom LLM instance."""
        fake_llm = FakeListLLM(responses=["test"])

        chain = get_conversation_chain(llm=fake_llm)

        assert chain.llm is fake_llm

    @patch("src.llm.chains.config")
    def test_get_conversation_chain_with_custom_memory(self, mock_config):
        """Test chain creation with a custom memory instance."""
        fake_llm = FakeListLLM(responses=["test"])
        custom_memory = get_conversation_memory()

        chain = get_conversation_chain(llm=fake_llm, memory=custom_memory)

        assert chain.memory == custom_memory

    @patch("src.llm.chains.config")
    def test_get_conversation_chain_with_custom_prompt(self, mock_config):
        """Test chain creation with a custom prompt template."""
        fake_llm = FakeListLLM(responses=["test"])
        custom_prompt = get_creative_prompt()

        chain = get_conversation_chain(llm=fake_llm, prompt_template=custom_prompt)

        assert chain.prompt == custom_prompt

    @patch("src.llm.chains.config")
    def test_get_conversation_chain_verbose_flag(self, mock_config):
        """Test verbose flag is passed to the chain."""
        fake_llm = FakeListLLM(responses=["test"])

        chain = get_conversation_chain(llm=fake_llm, verbose=True)
        assert chain.verbose is True

        chain_quiet = get_conversation_chain(llm=fake_llm, verbose=False)
        assert chain_quiet.verbose is False
