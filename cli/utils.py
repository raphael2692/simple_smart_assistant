import jsonref
import json
import requests
from dotenv import load_dotenv
from dotenv import dotenv_values
from loguru import logger

load_dotenv()
config = dotenv_values(".env") 
logger.debug(f"Reading form env: {config.keys()}")

url = f"{config['BASE_URL']}/openapi.json"

response = requests.get(url).json()

with open("openapi.json", "w", encoding="utf-8") as f:
    json.dump(response, f, ensure_ascii=False, indent=4)

with open("./openapi.json", "r") as f:
    openapi_spec = jsonref.loads(
        f.read()
    )  # it's important to load with jsonref, as explained below

def openapi_to_functions(openapi_spec):
    functions = []

    for path, methods in openapi_spec["paths"].items():
        for method, spec_with_ref in methods.items():
            # 1. Resolve JSON references.
            spec = jsonref.replace_refs(spec_with_ref)

            # 2. Extract a name for the functions.
            function_name = spec.get("operationId")

            # 3. Extract a description and parameters.
            desc = spec.get("description") or spec.get("summary", "")

            schema = {"type": "object", "properties": {}}

            req_body = (
                spec.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if req_body:
                schema["properties"]["requestBody"] = req_body

            params = spec.get("parameters", [])
            if params:
                param_properties = {
                    param["name"]: param["schema"]
                    for param in params
                    if "schema" in param
                }
                schema["properties"]["parameters"] = {
                    "type": "object",
                    "properties": param_properties,
                }

            functions.append(
                {"name": function_name, "description": desc, "parameters": schema}
            )

    return functions


def get_functions():
    return openapi_to_functions(openapi_spec)
