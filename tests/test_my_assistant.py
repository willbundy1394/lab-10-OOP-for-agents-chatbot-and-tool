# tests/test_my_assistant.py
# Author: William Bundy

"""Tests for the PricingAssistant class and PriceValidator tool."""

from my_assistant import PricingAssistant
from my_tool import PriceValidator


def make_assistant():
    """Builds a fresh assistant with its own tool for each test"""
    tool = PriceValidator({"MW-100": "$22.99", "MW-200": "$34.99"})
    return PricingAssistant("DataPipelineBot", "Validate prices", tool)


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
    assert "which SKU?" in reply


def test_assistant_handoff_to_supervisor():
    """Test that handoff words trigger to get a human supervisor."""
    bot = make_assistant()
    reply = bot.respond("I have a supervisor issue with my order")
    assert "supervisor" in reply
