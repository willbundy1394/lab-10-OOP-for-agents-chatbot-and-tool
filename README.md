# Lab 10: Pricing Validation Assistant

## Overview
A Python chatbot that checks product prices and flags special requests for a supervisor.

## How It Works
- my_tool.py: Stores SKU's and prices, then looks them up.
- my_assistant.py: Reads user messages, checks prices, and sends unsolvable issues to a supervisor.
- my_main.py: Runs a terminal chat loop so you can talk to the bot.
- tests/test_my_assistant.py: Runs unit tests to make sure everything works.

## How to Test
Run this command in your terminal:

ruff format . && ruff check . && pytest -v

