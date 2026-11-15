# Lab 10: Pricing Validation Assistant

## Overview
A Python chatbot that checks product prices and flags special requests for a supervisor.

## How It Works
- my_tool.py: Stores SKU's and prices, then looks them up.
- my_assistant.py: Reads user messages, checks prices, and sends unsolvable issues to a supervisor.
- my_main.py: Runs a terminal chat loop so you can talk to the bot.
- tests/test_my_assistant.py: Runs unit tests to make sure everything works.
- price_change_queue.py: Stores pending price change requests until staff approve or reject them.
- pricing_toolbox.py: Checks every tool request from the model to make sure the customer actually provided the SKU and new price.

## How to Test
Run this command in your terminal:

ruff format . && ruff check . && pytest -v

## Lab 11 - Local Model

The model answered pretty good when asked about approved discount levels it correctly listed 5%, 10%, and 15% from the instructions. It sometimes tried to invent a price when asked about an unknown SKU instead of saying it did not know. I kept price lookups and handoff words (refund, complaint, supervisor, issue) in code because those answers have to be exact and should never come from the model. Everything else is left to the model so the assistant can still hold a normal conversation.

## Lab 12 - Tools and Approval Queue

The model handled basic price lookups for valid SKUs like MW-100 really well by calling lookup_price on its own and returning the exact price. But the toolbox refused any request where the model tried to look up or change a made up SKU or price that the customer never actually typed in the chat. It also blocks any price changes from going through automatically until a staff member approves them in the queue at the end of my_main.py. To keep the model from making things up, I had to add rules to Instructions on main.py telling it that prices must only come from the price tool and to offer a supervisor if it does not know the answer. My keyword handoff rules for words like refund or supervisor also still work right away without asking the model.


