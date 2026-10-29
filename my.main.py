# my_main.py
# Author: Will Bundy

"""Chat script for testing the PricingAssistant in the terminal"""

from my_assistant import PricingAssistant
from my_tool import PriceValidator

PRICES = {
    "MW-100: $22.99",
    "MW-200: $34.99",
    "Mw-300: $10.99",
}

price_tool = PriceValidator(PRICES)
bot = PricingAssistant(
    "DataPipelineBot",
    "You are a helpful assistant that validates prices.",
    price_tool,
)

print("Type a message, or type quit to exit.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
