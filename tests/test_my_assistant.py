# tests/test_my_assistant.py
# Author: Will Bundy

"""Tests for the PricingAssistant class and related tools."""

from fake_model import FakeModel
from my_assistant import PricingAssistant
from my_tool import PriceValidator
from price_change_queue import PriceChangeQueue
from pricing_toolbox import PricingToolbox


class SilentModel:
    """A model that never has an answer."""

    def decide(self, instructions, history, tools):
        return None


def make_tools():
    """Build fresh tools for each test."""
    prices = {"MW-100": "$22.99", "MW-200": "$34.99"}
    price_tool = PriceValidator(prices)
    change_queue = PriceChangeQueue(price_tool)
    return PricingToolbox(price_tool, change_queue)


def make_assistant(model):
    """Build a fresh assistant with the given model."""
    return PricingAssistant("DataPipelineBot", "Validate prices.", make_tools(), model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_lookup_price_tool():
    tools = make_tools()
    assert "22.99" in tools.price_tool.lookup_price("MW-100")
    assert "no sku" in tools.price_tool.lookup_price("MW-999").lower()


def test_price_change_waits_for_approval():
    tools = make_tools()
    tools.change_queue.request_price_change("MW-100", "$19.99")
    assert len(tools.change_queue.waiting()) == 1
    assert tools.price_tool.base_prices["MW-100"] == "$22.99"  # not changed yet


def test_approve_makes_the_change_once():
    tools = make_tools()
    tools.change_queue.request_price_change("MW-100", "$19.99")
    assert tools.change_queue.approve(1) == "Request 1 approved."
    assert tools.price_tool.base_prices["MW-100"] == "$19.99"
    assert tools.change_queue.approve(1) == "Request 1 is already approved."


def test_made_up_sku_is_refused():
    model = FakeModel(
        [
            ask_for_tool("lookup_price", {"sku": "MW-999"}),
            {"text": "I need a valid SKU."},
        ]
    )
    bot = make_assistant(model)
    bot.respond("What is the price of MW-100?")  # customer never said MW-999
    assert "has not given that SKU" in bot.history[1]["content"]


def test_handoff_still_works():
    bot = make_assistant(FakeModel([]))
    assert "supervisor" in bot.respond("I have a complaint about pricing")


def test_safe_reply_when_model_is_down():
    bot = make_assistant(SilentModel())
    assert "try again" in bot.respond("hello")
