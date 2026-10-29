# my_assistant.py
# Author: Will Bundy

HANDOFF_WORDS = ["issue", "refund", "supervisor", "complaint"]


class PricingAssistant:
    """A pricing validation assistant inspired by my work in automated data pipelines"""

    def __init__(self, name, instructions, price_tool):
        """Set up the assistant with a name, instructions, tool, and history"""
        self.name = name
        self.instructions = instructions
        self.price_tool = price_tool
        self.history = []

    def respond(self, user_message):
        """Record the user message. choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a response based on keywords and the tool lookup"""
        text = user_message.lower()
        if self.needs_human(text):
            return "I am handing this off to our teams supervisor"
        if "hello" in text:
            return f"Hello! I am {self.name}. I can check a price for you."
        if "price" in text or "sku" in text:
            return self.price_reply(user_message)
        return "I'm not sure how to help you with that. I can check a price for you."

    def needs_human(self, text):
        """Return True if any handoff word is in text"""
        for word in HANDOFF_WORDS:
            return word in text

    def price_reply(self, user_message):
        """Look up SKU in tool and return standard price"""
        sku = self.price_tool.find_sku(user_message)
        if sku is None:
            return "which SKU? Please name a valid part number"
        price = self.price_tool.get_standard_price(sku)
        return f"The standard price for {sku} is {price}"
