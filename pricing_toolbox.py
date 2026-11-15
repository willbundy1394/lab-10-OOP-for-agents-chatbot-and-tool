# pricing_toolbox.py
# Author: Will Bundy


class PricingToolbox:
    """Every tool request from the model comes through here and is checked."""

    def __init__(self, price_tool, change_queue):
        """Hold the tools the model is allowed to ask for."""
        self.price_tool = price_tool
        self.change_queue = change_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.price_tool.lookup_price,
            self.change_queue.request_price_change,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "lookup_price":
            sku = self.clean(arguments, "sku")
            if sku == "":
                return "The SKU is missing. Ask the customer for it."
            if not self.customer_said(history, sku):
                return "The customer has not given that SKU. Ask them for it."
            return self.price_tool.lookup_price(sku)

        if name == "request_price_change":
            sku = self.clean(arguments, "sku")
            new_price = self.clean(arguments, "new_price")
            if sku == "" or new_price == "":
                return "Both the SKU and the new price are needed."
            if not self.customer_said(history, sku):
                return "The customer has not given that SKU. Ask them for it."
            if not self.customer_said(history, new_price):
                return "The customer has not given that price. Ask them for it."
            return self.change_queue.request_price_change(sku, new_price)

        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Return True if text appears in a message the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
