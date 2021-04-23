import os
import logging

logger = logging.getLogger("HOWTO")


class Howto:

    def __init__(self, **kwargs):
        """
        Creates a new Howto instance.
        """
        self.scenario_path = kwargs.get('scenario_path', None)

    def init_file(self, scenario_path):
        if os.path.exists(scenario_path):
            logger.info(f"Nice, {scenario_path} was found !")
        else:
            logger.error(f"{scenario_path} doesn't exist !")


"""
EXPORTED FUNCTIONS
=============================================================================
Those are the functions we really mean to export
"""

def howtoFromFile(**kwargs):
    howto = Howto(**kwargs)
    howto.init_file(
        kwargs.get("scenario_path", None)
    )
