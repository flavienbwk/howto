import os
import logging
import traceback

from PyInquirer import prompt

from . import utils

logger = logging.getLogger("HOWTO")


class Howto:

    def __init__(self, **kwargs):
        """
        Creates a new Howto instance.
        """
        self.scenario_path = kwargs.get('scenario_path', None)
        self.scenario = None

    def init_file(self, scenario_path):
        if os.path.exists(scenario_path):
            logger.info(f"Trying to load {scenario_path}...")
            scenario = utils.load_json_file(scenario_path)
            if scenario:
                self.scenario = scenario
            else:
                raise Exception(f"{scenario_path} has invalid JSON content.")
        else:
            raise Exception(f"{scenario_path} doesn't exist !")

    def validate_scenario(self):
        pass

    def run_scenario(self):
        answers = prompt.prompt(self.scenario.scenario, style=self.scenario.style)
        print('Order receipt:')
        pprint(answers)


"""
EXPORTED FUNCTIONS
================================================
Those are the functions we really mean to export
"""

def howtoFromFile(**kwargs):
    howto = Howto(**kwargs)
    try:
        howto.init_file(
            kwargs.get("scenario_path", None)
        )
        howto.validate_scenario()
        howto.run_scenario()
    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_stack())
