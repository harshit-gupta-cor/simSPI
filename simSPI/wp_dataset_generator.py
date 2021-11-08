import os,sys
import argparse
from config import Config as cfg
from wp_utils import wp_simulator
import mrcfile


#could be sent to iospi
parser = argparse.ArgumentParser()
parser.add_argument('config', default="Configs/parameters_generate_dataset.cfg", help="Specify config file", metavar="FILE")
args = parser.parse_args()
config=cfg(args.config)

def starfilesaver(image_number,image_path, params):
    pass

def paths(config):
    config.output_path = os.path.join(os.getcwd(), config.output_path)
    if os.path.exists(config.output_path) == False: os.mkdir(config.output_path)

    # save the arguments to a file
    with open(os.path.join(config.output_path , 'config.cfg'), 'w') as fp:
        config.config.write(fp)
    with open(os.path.join(config.output_path , 'config.txt'), 'w') as fp:
        config.config.write(fp)

#######################


paths(config)
simulator=wp_simulator(config)

for iterations in range(config.datasetSize//config.chunks):
    projections, params=simulator()
    for num,proj in enumerate(projections):
        image_number=config.chunks*iterations+num
        image_path=os.path.join(config.output_path,str(image_number).zfill(6)+".mrc")
        with mrcfile.new(image_path,overwrite="True") as m:
            m.set_data(projections[num].detach().cpu().numpy())
        starfilesaver(image_number,image_path, params)
        if image_number%100==0:
            print(image_number+1)



