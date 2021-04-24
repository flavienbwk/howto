import os
import sys
import signal
import logging
import traceback
from pathlib import Path

from PyInquirer import prompt, style_from_dict
from . import utils, addons
from . import validators  # used for validating prompts

logger = logging.getLogger("HOWTO")


class Howto:
    def __init__(self, **kwargs):
        """
        Creates a new Howto instance.
        """
        self.scenario_path = kwargs.get("scenario_path", None)
        self.scenario_parent = None
        self.scenario = None

    def init_file(self, scenario_path):
        if os.path.exists(scenario_path):
            logger.debug(f"Trying to load {scenario_path}...")
            scenario = utils.load_json_file(scenario_path)
            if scenario:
                self.scenario = scenario
                self.scenario_parent = Path(scenario_path).parent.absolute()
            else:
                raise Exception(f"{scenario_path} has invalid JSON content.")
        else:
            raise Exception(f"{scenario_path} doesn't exist !")

    def validate_scenario(self):
        """Validates required parameters in JSON scenario file"""
        if "name" not in self.scenario:
            raise Exception(f"No 'name' parameter was found in scenario")
        if "description" not in self.scenario:
            logger.debug(f"No 'description' parameter was provided in scenario")
            self.scenario["description"] = "_No description provided_"
        if "author" not in self.scenario:
            logger.debug(f"No 'author' parameter was provided in scenario")
            self.scenario["author"] = "_Unknown_"
        if "scenario" not in self.scenario:
            raise Exception(f"No 'scenario' parameter was found in scenario")
        if not isinstance(self.scenario["scenario"], list):
            raise Exception(f"'scenario' parameter is not a list")
        logger.debug("Scenario file correctly formatted")

    def format_scenario(self):
        """Transcripts specific PyInquirer properties to Python code"""
        for i, item in enumerate(self.scenario["scenario"]):
            for filter in ["validate", "filter", "when"]:
                if filter in item:
                    try:
                        self.scenario["scenario"][i][filter] = eval(item[filter])
                    except Exception as e:
                        raise Exception(
                            f"In scenario item {i} : '{filter}'' has invalid value {item[filter]} : \n{e}"
                        )

    def run_introduction(self):
        introduction_vars = {
            "name": self.scenario["name"],
            "author": self.scenario["author"],
            "description": self.scenario["description"],
        }
        addons.ADDONS["markdown"](
            self,
            introduction_vars,
            {"markdown": f"{Path(__file__).parent}/INTRODUCTION.md"},
            use_parent=False,
        )
        input("Press a key to continue...")

    def run_scenario(self):
        all_answers = {}
        for i, item in enumerate(self.scenario["scenario"]):
            # Replace each scenario item properties using variables ("prompt", "message"...)
            self.scenario["scenario"][i] = utils.format_item_variables(
                item, all_answers
            )

            # Running addons
            skip_prompt = False
            for addon in addons.ADDONS:
                if addon in item.keys():
                    addons.ADDONS[addon](self, all_answers, item)
                    if addon in addons.SKIP_ON_FINISH_ADDONS:
                        skip_prompt = True
                    del self.scenario["scenario"][i][addon]
            if skip_prompt:
                continue

            # Run next prompt
            answers = prompt(
                questions=[self.scenario["scenario"][i]],
                answers=all_answers,
                # TODO(flavienbwk) Fix : style=style_from_dict(self.scenario["style"])
            )
            logger.debug(answers)

            # Handling CTRL+C (https://github.com/CITGuru/PyInquirer/issues/6)
            if not answers:
                signal_handler(signal.SIGINT, None)
            all_answers.update(answers)
        logger.debug("Summary :")
        logger.debug(all_answers)


def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN)
    logger.info("Quitting Howto")
    sys.exit(0)


"""
EXPORTED FUNCTIONS
================================================
Those are the functions we really mean to export
"""


def howtoFromFile(**kwargs):
    signal.signal(signal.SIGINT, signal_handler)

    howto = Howto(**kwargs)
    try:
        howto.init_file(kwargs.get("scenario_path", None))
        howto.validate_scenario()
        howto.format_scenario()
        howto.run_introduction()
        howto.run_scenario()
    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_exc())
