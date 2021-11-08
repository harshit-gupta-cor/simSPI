import torch
from torch import nn
import torch.fft


class wp_simulator(torch.nn.Module):
    def __init__(self, config, initial_volume=None):
        super(wp_simulator, self).__init__()
        '''module that generates data using weak phase approximation with a given config setting. 
            projector->ctf->shift->noise
        '''
        self.Projector = Projector(config) #tomographic projector
        self.init_volume(initial_volume)   #changes the volume inside the projector
        self.CTF = CTF(config)             #convolves ctf
        self.Shift = Shift(config)         #adds shifts
        self.Noise = Noise(config)         #adds noise
        self.config = config

    def forward(self):

        #generate the parameter of the forward model
        rotmat=self.rotmat_generator()
        ctf_params=self.ctf_generator()
        shift_params=self.shift_generator()
        noise_params=self.noise_generator()

        #apply the forward model
        projection=self.Projector(rotmat)
        f_projection=primal_to_fourier_2D(projection)
        f_projection=self.CTF(f_projection,ctf_params)
        f_projection=self.Shift(f_projection, shift_params)
        projection=fourier_to_primal_2D(f_projection)
        projection=self.Noise(projection, noise_params)

        return projection.real, {"rotmat": rotmat, "ctf_params":ctf_params, "shift_params": shift_params, "noise_params": noise_params  }

    def init_volume(self, initial_volume):
        pass

    def rotmat_generator(self):
        return {}

    def ctf_generator(self):
        return {}

    def shift_generator(self):
        return {}

    def noise_generator(self):
        return {}



class Projector(torch.nn.Module):
    def __init__(self, config):
        super(Projector, self).__init__()

        self.sidelen = config.sidelen
        self.vol_shape = [self.sidelen]*3
        self.vol = nn.Parameter(0.01 * torch.rand(self.vol_shape, dtype=torch.float32),
                                requires_grad=True)
        self.config=config

    # project and rotate
    def forward(self, rotmat):
        projection=self.vol.sum(0).repeat(self.config.chunks,1,1)[:, None, :,:]
        return projection

    def make_volume(self):
        return self.vol.detach()

class CTF(torch.nn.Module):
    def __init__(self, config):
        super(CTF, self).__init__()

        self.size = config.ctf_size
        self.resolution = config.resolution
        self.kV = config.kV
        self.valueNyquist = config.valueNyquist
        self.amplitudeContrast = config.amplitudeContrast
        self.frequency = 1. / (self.size * self.resolution)

    def forward(self, x_fourier, ctf_params={}):
        return x_fourier


class Shift(torch.nn.Module):

    def __init__(self, config):
        super(Shift, self).__init__()
        self.resolution=config.resolution

    def forward(self, x_fourier, shift_params={}):

        return x_fourier


class Noise(torch.nn.Module):
    def __init__(self, config):
        super(Noise, self).__init__()
        self.noise_sigma = config.noise_sigma

    def forward(self, proj, nosie_params={}):

        return proj


def primal_to_fourier_2D(r):
    r = torch.fft.fftshift(r, dim=(-2, -1))
    return torch.fft.ifftshift(torch.fft.fftn(r, s=(r.shape[-2], r.shape[-1]), dim=(-2, -1)), dim=(-2, -1))

def fourier_to_primal_2D(f):
    f = torch.fft.ifftshift(f, dim=(-2, -1))
    return torch.fft.fftshift(torch.fft.ifftn(f, s=(f.shape[-2], f.shape[-1]), dim=(-2, -1)), dim=(-2, -1))
