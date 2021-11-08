#imports wp simulator and generates data scpecified by the .cfg file
import os,sys
import argparse
from config import Config as cfg
from wp_utils import wp_simulator
import mrcfile


#=================could be sent to iospi

#takes the cfg file with parameters and creates a variable called config with those parameters
parser = argparse.ArgumentParser()
parser.add_argument('config', default="configs/parameters_generate_dataset.cfg", help="Specify config file", metavar="FILE")
args = parser.parse_args()
config=cfg(args.config)

#will be useful to create the starfile for the generated data
def starfilesaver(image_number,image_path, params):
    pass

# create the output folders and saving the .cfg file there
def paths(config):
    config.output_path = os.path.join(os.getcwd(), config.output_path)
    if os.path.exists(config.output_path) == False: os.mkdir(config.output_path)

    # save the arguments to a file
    with open(os.path.join(config.output_path , 'config.cfg'), 'w') as fp:
        config.config.write(fp)
    with open(os.path.join(config.output_path , 'config.txt'), 'w') as fp:
        config.config.write(fp)

#=================


paths(config)
simulator=wp_simulator(config)

#iterating to save the data over a loop
for iterations in range(config.datasetSize//config.chunks):
    projections, params=simulator()
    #iterating over the chunk of projections to save the mrcfiles. Chunks are being used to accelerate the data generation
    for num,proj in enumerate(projections):
        image_number=config.chunks*iterations+num
        image_path=os.path.join(config.output_path,str(image_number).zfill(6)+".mrc")
        with mrcfile.new(image_path,overwrite="True") as m:
            m.set_data(projections[num].detach().cpu().numpy())
        starfilesaver(image_number,image_path, params)
        if image_number%100==0:
            print(image_number+1)



