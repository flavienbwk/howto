import os
import re
import logging

from rich.console import Console
from rich.markdown import Markdown

logger = logging.getLogger("HOWTO")


def markdown(howto, all_answers: dict, scenario_item: dict, use_parent=True):
    markdown_path = (
        f"{howto.scenario_parent}/{scenario_item['markdown']}"
        if use_parent
        else scenario_item["markdown"]
    )
    logger.debug(f"addons.markdown: Loading file : {markdown_path}")
    console = Console()
    with open(markdown_path) as readme:
        text = readme.read()
    # Replacing variables
    for match in re.findall(r"\{\{(.*)\}\}", text):
        if match in all_answers:
            text = text.replace("{{" + match + "}}", all_answers[match])
        else:
            logger.debug(
                f"addons.markdown: Variable {match} not found for {markdown_path}"
            )
    console.print(Markdown(text))


def clear(howto, all_answers: dict, scenario_item: dict):
    os.system("clear")


# Exposed addons for JSON configuration
ADDONS = {"clear": clear, "markdown": markdown}
