import json
import os


def load_json_file(file_dir, json_filename):
    json_file_path = file_dir + "/" + json_filename
    if os.path.exists(json_file_path) is False:
        print("Directory {} has no {} file, ignoring".format(file_dir, json_filename))
        return False
    with open(json_file_path, "r") as json_file:
        json_content_file = json_file.read()
    json_element = json.loads(json_content_file)
    if json:
        print("Successfuly loaded {} from {}".format(file_dir, json_filename))
        return json_element
    else:
        print(
            "Directory {} has an invalid {} file, ignoring".format(
                file_dir, json_filename
            )
        )
        return False
