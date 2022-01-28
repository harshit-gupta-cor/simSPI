"""contain the main function to generate dataset."""
import argparse
import os
import sys
import traceback

from linear_simulator.params_utils import params_update

from .config import Config as cfg
from .dataset_generator import DatasetGenerator


def init_config():
    """Take the cfg file and creates an abject called config."""
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Specify config file", metavar="FILE")
    args = parser.parse_args()
    if not os.path.isfile(args.config):
        raise FileNotFoundError("Please provide a valid .cfg file")

    config = cfg(args.config)
    config = params_update(config)
    return config


def main():
    """Run the dataset generation."""
    config = init_config()
    dataset_generator = DatasetGenerator(config)
    dataset_generator.run()
    return 0, "Dataset successfully generated."


if __name__ == "__main__":
    try:
        retval, status_message = main()
    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
        print(e)
        retval = 1
        status_message = "Error: Training failed."

    print(status_message)
    exit(retval)
