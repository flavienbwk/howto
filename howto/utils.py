import re
import json


def format_item_variables(item: dict, variables: dict):
    for key in item.keys():
        if key in ["message", "prompt"]:
            item[key] = replace_variables(item[key], variables)
    return item


def load_json_file(json_file_path):
    with open(json_file_path, "r") as json_file:
        json_content_file = json_file.read()
    return json.loads(json_content_file)


def replace_variables(text: str, variables: dict):
    """Replaces all variables (declared as "{{my_variable}}")
    in a text with variables provided.

    Variables that are not provided are left untouched in the text.
    """

    for match in re.findall(r"\{\{(.*)\}\}", text):
        if match in variables:
            text = text.replace("{{" + match + "}}", variables[match])
    return text
