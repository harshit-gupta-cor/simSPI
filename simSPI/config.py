"""Load program configuration into a config object."""

from backports import configparser

"""Module to convert args into class with attributes."""


class Config(object):
    """Class to convert args into class with attributes.

    Parameters
    ----------
    filename: str
        path of the config file from which the attributes are loaded.

    """

    def __init__(self, filename):
        self.load_config(filename)

    def load_config(self, filename):
        """Load and save the config file."""
        config = configparser.SafeConfigParser()
        config.read(filename)
        self.config = config

        s = "general"
        self.name = config.get(s, "name")
        self.dataset_size = config.getint(s, "dataset_size")
        self.batch_size = config.getint(s, "batch_size")
        self.simulator = config.get(s, "simulator")

        s = "paths"
        self.input_volume_path = config.get(s, "input_volume_path")
        self.output_path = config.get(s, "output_path")
        self.input_starfile_path = config.get(s, "input_starfile_path")

        s = "projector"
        self.volume_domain = config.get(s, "volume_domain").lower()
        self.side_len = config.getint(s, "side_len")
        self.angle_distribution = config.get(s, "angle_distribution").lower()
        self.relion_invert_hand = config.getboolean(s, "relion_invert_hand")

        s = "ctf"
        self.ctf = config.getboolean(s, "ctf")
        self.change_ctfs = config.getboolean(s, "change_ctfs")
        self.ctf_size = config.getint(s, "ctf_size")
        self.value_nyquist = config.getfloat(s, "value_nyquist")
        self.b_factor = config.getfloat(s, "b_factor")
        self.pixel_size = config.getfloat(s, "pixel_size")
        self.kv = config.getfloat(s, "kv")
        self.cs = config.getfloat(s, "cs")
        self.amplitude_contrast = config.getfloat(s, "amplitude_contrast")
        self.min_defocus = config.getfloat(s, "min_defocus")
        self.max_defocus = config.getfloat(s, "max_defocus")

        s = "shift"
        self.shift = config.getboolean(s, "shift")
        self.shift_std_deviation = config.getfloat(s, "shift_std_deviation")
        self.shift_distribution = config.get(s, "shift_distribution").lower()

        s = "noise"
        self.noise = config.getboolean(s, "noise")
        self.noise_distribution = config.get(s, "noise_distribution").lower()
        self.noise_sigma = config.getfloat(s, "noise_sigma")
