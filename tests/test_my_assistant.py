# tests/test_my_assistant.py
# Author: William Bundy

"""Tests for the PricingAssistant class and PriceValidator tool."""

from mock_model import MockModel
from my_assistant import PricingAssistant
from my_tool import PriceValidator


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def reply(self, instructions, history):
        return None


def make_assistant():
    """Build a fresh assistant with its own tool and mock model for each test."""
    tool = PriceValidator({"MW-100": "$22.99", "MW-200": "$34.99"})
    return PricingAssistant("DataPipelineBot", "Validate prices", tool, MockModel())


def test_tool_finds_standard_price():
    """Test that the price lookup tool returns the right price."""
    tool = PriceValidator({"MW-100": "$22.99"})
    assert tool.get_standard_price("MW-100") == "$22.99"


def test_assistant_validates_sku_price():
    """Test that the assistant responds with the product price."""
    bot = make_assistant()
    reply = bot.respond("Can you check price for MW-100?")
    assert "$22.99" in reply


def test_assistant_handles_unknown_sku():
    """Test that the assistant asks for a valid SKU when an unknown product is provided."""
    bot = make_assistant()
    reply = bot.respond("Check price for MW-999")
    assert "SKU" in reply


def test_assistant_handoff_to_supervisor():
    """Test that handoff words trigger a human supervisor."""
    bot = make_assistant()
    reply = bot.respond("I have a supervisor issue with my order")
    assert "supervisor" in reply


def test_other_messages_go_to_the_model():
    """Test that messages with no rule go to the model."""
    bot = make_assistant()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_unknown_request_gets_a_safe_reply():
    """Test the safe reply when the model has no answer."""
    tool = PriceValidator({"MW-100": "$22.99"})
    bot = PricingAssistant("DataPipelineBot", "Validate prices", tool, SilentModel())
    assert "try again" in bot.respond("What is your favorite color?")
