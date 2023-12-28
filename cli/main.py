from setup import chat_with_memory, avaiable_functions, functions
from dotenv import load_dotenv
from dotenv import dotenv_values
from loguru import logger
from datetime import date

load_dotenv()
config = dotenv_values(".env") 

messages = []
system_prompt = f"""
Current date: {date.today()}
Settings: {config['SYSTEM_PROMPT']}
"""
messages.append({"role": "system", "content": system_prompt})

while True:
    message = input("USER: ")
    messages.append({"role": "user", "content": message })
    chat_with_memory(messages, avaiable_functions=avaiable_functions, functions=functions)
