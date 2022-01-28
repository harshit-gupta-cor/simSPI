"""run dataset generator and save it."""
import os

import torch
from ioSPI.save_utils import save_mrc, save_starfile_cryoem_convention
from ioSPI.starfile_utils import starfile_data
from simulator_factory import SimulatorFactory

from .linear_simulator.params_utils import ParamsFactory

"""Module to generate and save dataset (including metadata) in the output directory."""


class DatasetGenerator(torch.nn.Module):
    """class to generate and save dataset (including metadata) in the output directory.

    Parameters
    ----------
    config: class
        Class containing parameters of the dataset generation and simulator.

    """

    def __init__(self, config):
        super(DatasetGenerator, self).__init__()

        self.config = config
        self.simulator = SimulatorFactory.get_simulator(
            config
        )  # instantiating the simulator
        self.dataframe = []
        self.init_dir()  # initializing the output folder
        self.print_statements()
        self.params_generator = ParamsFactory.get_params_generator(
            config
        )  # instantiating params generator

    def run(self):
        """Generate a chunk of projection and save it."""
        datalist = []
        for iterations in range(self.config.datasetSize // self.config.batch_size):
            rot_params, ctf_params, shift_params = self.params_generator.get_params()
            projections = self.simulator(rot_params, ctf_params, shift_params)
            save_mrc(self.config.output_path, projections, iterations)
            datalist = starfile_data(
                datalist, rot_params, ctf_params, shift_params, iterations, self.config
            )

        print(f"Saving star file with the parameters of the generated dataset..")
        save_starfile_cryoem_convention(
            self.config.output_path, datalist, self.config, save_name="Simulated"
        )

    def init_dir(self):
        """Make the output directory and puts the path in the config.output_path."""
        self.config.output_path = os.path.join(os.getcwd(), self.config.output_path)

        self.config.output_path = os.path.join(self.config.output_path, "Datasets")
        if os.path.exists(self.config.output_path) is False:
            os.mkdir(self.config.output_path)

        self.config.output_path = os.path.join(
            self.config.output_path, self.config.name
        )
        if os.path.exists(self.config.output_path) is False:
            os.mkdir(self.config.output_path)

    def print_statements(self):
        """Print statements about the data."""
        print(f"The size of the dataset is {self.config.datasetSize}")
        L = self.config.sidelen
        print(f"Size of the volume is {L}x{L}x{L}")
        print(
            f"Size of each projection is {self.config.sidelen}x{self.config.sidelen}\n"
        )
        print(f"Output directory is '{self.config.output_path}'\n")
