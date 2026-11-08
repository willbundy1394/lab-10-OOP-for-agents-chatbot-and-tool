# my_assistant.py
# Author: Will Bundy

HANDOFF_WORDS = ["issue", "refund", "supervisor", "complaint"]


class PricingAssistant:
    """A pricing validation assistant inspired by my work in automated data pipelines."""

    def __init__(self, name, instructions, price_tool, model):
        """Set up the assistant with a name, instructions, tool, model, and history."""
        self.name = name
        self.instructions = instructions
        self.price_tool = price_tool
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Record the user message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use a rule when one applies. Otherwise ask the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I am handing this off to our team's supervisor."
        if "price" in text or "sku" in text:
            return self.price_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply

    def needs_human(self, text):
        """Return True if any handoff word is in text."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def price_reply(self, user_message):
        """Look up SKU in tool and return standard price."""
        sku = self.price_tool.find_sku(user_message)
        if sku is None:
            return "Which SKU? Please name a valid part number."
        price = self.price_tool.get_standard_price(sku)
        return f"The standard price for {sku} is {price}."
