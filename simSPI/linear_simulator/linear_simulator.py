"""contains simulator and its components classes."""

import os

import mrcfile
import torch
from compSPI.src.transforms import fourier_to_primal_2D, primal_to_fourier_2D
from ctf import CTF
from noise_utils import Noise
from projector import Projector
from shift_utils import Shift
from volume_utils import init_cube

"""Module to generate data using using liner forward model."""


class LinearSimulator(torch.nn.Module):
    """Class to generate data using liner forward model.

    Parameters
    ----------
    config: class
        Class containing parameters of the simulator

    """

    def __init__(self, config, initial_volume=None):
        super(LinearSimulator, self).__init__()

        self.config = config
        self.projector = Projector(config)  # class for tomographic projector
        self.init_volume()  # changes the volume inside the projector
        self.ctf = CTF(config)  # class for ctf
        self.shift = Shift(config)  # class for shifts
        self.noise = Noise(config)  # class for noise

    def forward(self, rot_params, ctf_params, shift_params):
        """Create cryoEM measurements using input parameters.

        Parameters
        ----------
        rot_params: dict of type str to {tensor}
            Dictionary of rotation parameters for a projection chunk
        ctf_params: dict of type str to {tensor}
            Dictionary of Contrast Transfer Function (CTF) parameters
             for a projection chunk
        shift_params: dict of type str to {tensor}
            Dictionary of shift parameters for a projection chunk

        Returns
        -------
        projection.real : tensor
            Tensor ([chunks,1,sidelen,sidelen]) contains cryoEM measurement
        """
        projection = self.Projector(rot_params)
        f_projection = primal_to_fourier_2D(projection)
        f_projection = self.CTF(f_projection, ctf_params)
        f_projection = self.Shift(f_projection, shift_params)
        projection = fourier_to_primal_2D(f_projection)
        projection = self.Noise(projection)

        return projection.real

    def init_volume(self):
        """Initialize the volume inside the projector.

        Initializes the mrcfile whose path is given in config.input_volume_path.
        If the path is not given or doesn't exist then the volume
        is initialized with a cube.
        """
        if (
            self.config.input_volume_path == ""
            or os.path.exists(os.path.join(os.getcwd(), self.config.input_volume_path))
            is False
        ):

            print(
                "No input volume specified or the path doesn't exist. "
                "Using cube as the default volume."
            )
            volume = init_cube(self.config.sidelen)
        else:
            with mrcfile.open(self.config.input_volume_path, "r") as m:
                volume = torch.from_numpy(m.data.copy()).to(self.Projector.vol.device)

        self.Projector.vol = volume
