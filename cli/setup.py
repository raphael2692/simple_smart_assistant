import openai
import sys
import json
from utils import get_functions
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
from utils import logger

load_dotenv()

config = dotenv_values(".env") 
logger.debug(f"Using the following configuration: {config}")

functions = get_functions()
logger.debug(f"Using the following functions: {functions}")


def chat_with_memory(messages:list, avaiable_functions:dict, functions:list) -> None:
    # Create first response using functions
    response = openai.OpenAI().chat.completions.create(
        model=config["MODEL"],
        messages=messages,
        functions = functions,
        function_call = 'auto' # on 'auto' CahtGPT decides if using given functions or not
    )

    # ChatGPT try to use functions
    if response.choices[0].message.function_call:
        function_name = response.choices[0].message.function_call.name
        function_args = json.loads(response.choices[0].message.function_call.arguments)
        function_response = avaiable_functions[function_name](**function_args)
        messages.append({"role": "system", "content": function_response})
    else:
        messages.append({"role": "system", "content": "Unable to process request." })
    
    # Create second response, to make ChatGPT process that output
    response = openai.OpenAI().chat.completions.create(
        model=config["MODEL"],
        messages=messages # Note how messages are chained
    )
    response = response.choices[0].message.content
    # Add response to history
    messages.append({"role": "system", "content": response})
    # Display output in the console
    print("*CHATBOT* :", response)

def read_todos_todos_get(**kwargs):
    logger.debug(kwargs)
    url = f"{config['BASE_URL']}/todos"
    return f"{requests.get(url).json()}"

def create_todo_todos_post(**kwargs):
    logger.debug(kwargs)
    body = kwargs["requestBody"]
    url = f"{config['BASE_URL']}/todos"
    return f"{requests.post(url, json=body).json()}"

def update_todo_todos__todo_id__put(**kwargs):
    logger.debug(kwargs)
    id = kwargs["parameters"]["todo_id"]
    done = kwargs["parameters"]["done"]
    base_url = f"http://localhost:8000/todos/{id}?done={done}"
    return f'{requests.put(base_url).json()}'

def delete_todo_todos__todo_id__delete(**kwargs):
     logger.debug(kwargs)
     id = kwargs["parameters"]["todo_id"]
     base_url = f"http://localhost:8000/todos/{id}"
     return f"{requests.delete(base_url).json()}"

avaiable_functions = {
    "read_todos_todos_get": read_todos_todos_get,
    "create_todo_todos_post": create_todo_todos_post,
    "update_todo_todos__todo_id__put": update_todo_todos__todo_id__put,
    "delete_todo_todos__todo_id__delete": delete_todo_todos__todo_id__delete
}