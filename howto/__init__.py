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
        if len(self.scenario["scenario"]) == 0:
            raise Exception(f"No scenario steps were found")
        if not isinstance(self.scenario["scenario"], list):
            raise Exception(f"'scenario' parameter is not a list")
        logger.debug("Scenario file correctly formatted")

    def format_scenario(self):
        """Transcripts specific PyInquirer properties to Python code"""
        for i, step in enumerate(self.scenario["scenario"]):
            if "name" not in step:
                raise Exception(
                    f"No 'name' found for step {i} in scenario {self.scenario['name']}"
                )
            for filter in ["validate", "filter", "when"]:
                if filter in step:
                    try:
                        self.scenario["scenario"][i][filter] = eval(step[filter])
                    except Exception as e:
                        raise Exception(
                            f"In scenario step {i} : '{filter}'' has invalid value {step[filter]} : \n{e}"
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
        steps = utils.format_steps_by_name(self.scenario["scenario"])
        stack = [name for name, _ in steps.items()]

        while len(stack):
            step_name = stack[0]
            step = steps[step_name].copy()
            logger.debug(f"Running step {step_name}")

            # Replace each scenario step properties using variables ("prompt", "message"...)
            step = utils.format_step_variables(step, all_answers)

            # Running addons
            skip_prompt = False
            for addon in addons.ADDONS:
                if addon in step.keys():
                    addons.ADDONS[addon](self, all_answers, step)
                    if addon in addons.SKIP_ON_FINISH_ADDONS:
                        skip_prompt = True
                    del step[addon]

            if skip_prompt == False:
                # Run next prompt
                answers = prompt(questions=[step], answers=all_answers)
                logger.debug(answers)

                # Handling CTRL+C (https://github.com/CITGuru/PyInquirer/issues/6)
                if not answers:
                    signal_handler(signal.SIGINT, None)

                all_answers.update(answers)

            # Pop current step
            stack.pop(0)

            # Process direct and conditional jumps
            if "jump" in step:
                next_step = None
                if isinstance(step["jump"], str):
                    # Direct jumps
                    next_step = step["jump"]
                elif step_name in answers and str(answers[step_name]) in step["jump"]:
                    # Conditional jump (by value)
                    next_step = step["jump"][str(answers[step_name])]
                    # Removing other step choices : the chosen one will be inserted in stack
                    for other_step in [value for _, value in step["jump"].items()]:
                        if other_step in stack:
                            stack.remove(other_step)
                if next_step and stack[0] != next_step:
                    stack.insert(0, next_step)

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
