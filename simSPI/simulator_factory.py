"""contain simulator factory from which simulator can be chosen."""
from abc import ABCMeta, abstractstaticmethod

import tem
from linear_simulator import linear_simulator

"""Module to instantiate simulator from a factory of choices."""


class SimulatorFactory:
    """Class to instantiate simulator from a factory of choices."""

    def get_simulator(config):
        """Return the simulator class.

        Parameters
        ----------
        config: class
        Returns
        -------
        params_generator: class
        """
        if config.simulator == "linear":
            return linear_simulator.LinearSimulator(config)
        else:
            return tem.TEMSimulator(config)


class Isimulator(metaclass=ABCMeta):
    """Abstract class for the simulator factory with forward method."""

    @abstractstaticmethod
    def forward(self):
        """Get the projections."""
