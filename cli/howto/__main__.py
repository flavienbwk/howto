import howto
import sys
import warnings
import argparse
import pkg_resources

import logging
from logging import DEBUG, INFO, WARNING

from . import logger

logger = logging.getLogger("HOWTO")


def parse_options(args=None, values=None):
    """
    Define and parse `optparse` options for command-line usage.
    """
    parser = argparse.ArgumentParser(
        description="Multi-scenarios CLI tool for tutorials, guides or stories. More help at : https://github.com/flavienbwk/howto."
    )
    parser.add_argument("file", type=str, help="JSON scenario file path")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=DEBUG,
        dest="verbosity",
        default=INFO,
        help="Print all operations.",
    )
    args = parser.parse_args()

    parameters = {"scenario_path": args.file}

    return parameters, args.verbosity


def run():
    """Run howto from the command line."""

    # Parse options and adjust logging level if necessary
    options, logging_level = parse_options()
    if not options:
        sys.exit(2)
    logger.setLevel(logging_level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logger_utils.Formatter())
    logger.addHandler(console_handler)
    if logging_level <= WARNING:
        # Ensure deprecation warnings get displayed
        warnings.filterwarnings("default")
        logging.captureWarnings(True)
        warn_logger = logging.getLogger("py.warnings")
        warn_logger.addHandler(console_handler)

    # Welcome message
    version = pkg_resources.require("howto-cli")[0].version
    logger.info(f"Welcome to howto {version} !")

    # Run
    howto.howtoFromFile(**options)


if __name__ == "__main__":
    run()
