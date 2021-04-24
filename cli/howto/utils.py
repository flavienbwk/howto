import json
import os


def load_json_file(json_file_path):
    with open(json_file_path, "r") as json_file:
        json_content_file = json_file.read()
    return json.loads(json_content_file)
