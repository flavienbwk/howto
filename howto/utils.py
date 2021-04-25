import re
import json

def format_steps_by_name(scenario: list):
    steps = {}
    for step in scenario:
        steps[step["name"]] = step
    return steps

def format_step_variables(step: dict, variables: dict):
    for key in step.keys():
        if key in ["message", "prompt"]:
            step[key] = replace_variables(step[key], variables)
    return step


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
            replacement = str(variables[match])
            text = text.replace("{{" + match + "}}", replacement)
    return text
