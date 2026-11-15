# price_change_queue.py
# Author: Will Bundy


class PriceChangeQueue:
    """Price changes waiting for approval. Nothing changes until they are approved."""

    def __init__(self, price_validator):
        """Start with no requests. Approved changes go through the price validator."""
        self.price_validator = price_validator
        self.requests = []

    def request_price_change(self, sku, new_price):
        """Ask staff to change the approved price for one SKU. Staff must approve it.

        Args:
            sku: The part number/SKU, like MW-100.
            new_price: The new approved price.
        """
        found_sku = self.price_validator.find_sku(sku)
        if found_sku is None:
            return "No SKU with that part number was found. SKUs look like MW-100."
        number = len(self.requests) + 1
        request = {
            "number": number,
            "sku": found_sku,
            "new_price": new_price,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to staff. The price has not changed yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and make the change."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.price_validator.change_price(request["sku"], request["new_price"])
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing changes."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
