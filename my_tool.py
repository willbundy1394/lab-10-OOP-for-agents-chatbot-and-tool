# my_tool.py
# Author: Will Bundy


class PriceValidator:
    """A tool that looks up approved standard prices for part numbers/SKUs."""

    def __init__(self, base_prices):
        """Save the dictionary of product SKUs and their approved prices."""
        self.base_prices = base_prices

    def find_sku(self, text):
        """Return the first known SKU mentioned in text, or None."""
        for sku in self.base_prices:
            if sku.lower() in text.lower():
                return sku
        return None

    def get_standard_price(self, sku):
        """Return the approved price for one SKU, or None if unknown."""
        for key in self.base_prices:
            if key.lower() == sku.lower():
                return self.base_prices[key]
        return None
