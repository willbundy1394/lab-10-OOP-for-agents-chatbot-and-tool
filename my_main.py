# my_main.py
# Author: Will Bundy

from fallback_model import FallbackModel
from keyword_model import KeywordModel
from my_assistant import PricingAssistant
from my_tool import PriceValidator
from ollama_model import OllamaModel
from price_change_queue import PriceChangeQueue
from pricing_toolbox import PricingToolbox

BASE_PRICES = {
    "MW-100": "$22.99",
    "MW-200": "$34.99",
    "MW-300": "$15.50",
}

INSTRUCTIONS = """You are DataPipelineBot, a pricing validation assistant.
Answer in one short sentence.
Approved discount levels are 5%, 10%, and 15%.
Prices must only come from the price tool — never invent a price.
If the client only says hello, greet them and ask how you can help.
Only state facts that appear in these instructions or in tool results.
If you do not know, say you do not know and offer to pass the customer to a supervisor."""

price_tool = PriceValidator(BASE_PRICES)
change_queue = PriceChangeQueue(price_tool)
tools = PricingToolbox(price_tool, change_queue)

# Use Fallback so it still works when Ollama is off
model = FallbackModel(OllamaModel("granite4.1:3b"), KeywordModel())

bot = PricingAssistant("DataPipelineBot", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in change_queue.waiting():
    number = request["number"]
    print(f"Request {number}: {request['sku']} → {request['new_price']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(change_queue.approve(number))
    else:
        print(change_queue.reject(number))

print("Current prices:")
for sku, price in BASE_PRICES.items():
    print(sku, price)
