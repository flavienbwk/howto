import os
import re
import logging

from rich.console import Console
from rich.markdown import Markdown

from . import utils

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
    text = utils.replace_variables(text, all_answers)
    console.print(Markdown(text))


def clear(howto, all_answers: dict, scenario_item: dict):
    os.system("clear")


def prompt(howto, all_answers: dict, scenario_item: dict):
    input(scenario_item["prompt"])


# Exposed addons for JSON configuration
ADDONS = {"clear": clear, "markdown": markdown, "prompt": prompt}

# Addons that won't pass the hand to PyInquirer
SKIP_ON_FINISH_ADDONS = ["prompt"]
