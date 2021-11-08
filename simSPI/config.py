""" Loads program configuration into a config object."""

from backports import configparser


class Config(object):
    def __init__(self, filename):
        self.load_config(filename)

    def load_config(self, filename):
        config = configparser.SafeConfigParser()
        config.read(filename)
        self.config = config

        s = "general"
        self.name = config.get(s, 'name')
        self.datasetSize = config.getint(s, 'datasetSize')
        self.chunks = config.getint(s, 'chunks')

        s = "paths"
        self.input_volume_path=config.get(s, 'input_volume_path').lower()
        self.output_path = config.get(s, 'output_path').lower()
        self.input_star_file_path = config.get(s, 'input_star_file_path').lower()
        self.output_star_file_path = config.get(s, 'output_star_file_path').lower()
        self.input_star_file = config.getboolean(s, 'input_star_file')
        self.output_star_file = config.getboolean(s, 'output_star_file')

        s="projector"
        self.volumedomain = config.get(s, 'volumedomain').lower()
        self.sidelen = config.getint(s, 'sidelen')
        self.angle_distribution = config.get(s, 'angle_distribution').lower()

        s="ctf"
        self.ctf = config.getboolean(s, 'ctf')
        self.changectfs = config.getboolean(s, 'changectfs')
        self.ctf_size = config.getint(s, 'ctf_size')
        self.valueNyquist = config.getfloat(s, 'valueNyquist')
        self.resolution = config.getfloat(s, 'resolution')
        self.kV = config.getfloat(s, 'kV')
        self.amplitudeContrast= config.getfloat(s, 'amplitudeContrast')

        s="translation"
        self.translation = config.getboolean(s, 'translation')
        self.translationVariance = config.getfloat(s, 'translationVariance')
        self.translation_distribution = config.get(s, 'translation_distribution').lower()

        s="noise"
        self.noise = config.getboolean(s, 'noise')
        self.noise_distribution = config.get(s, 'noise_distribution').lower()
        self.noise_sigma = config.getfloat(s, 'noise_sigma')


