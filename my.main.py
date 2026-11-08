# my_main.py
# Author: Will Bundy

from my_assistant import PricingAssistant
from my_tool import PriceValidator
from ollama_model import OllamaModel

BASE_PRICES = {
    "MW-100": "$22.99",
    "MW-200": "$34.99",
    "MW-300": "$15.50",
}

INSTRUCTIONS = """You are DataPipelineBot, a pricing validation assistant.
Answer in one short sentence.
Approved discount levels are 5%, 10%, and 15%.
Prices must only come from the price tool never invent a price.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to a supervisor."""

price_tool = PriceValidator(BASE_PRICES)
model = OllamaModel("granite4.1:3b")
bot = PricingAssistant("DataPipelineBot", INSTRUCTIONS, price_tool, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
