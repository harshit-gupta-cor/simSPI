Activate the simSPI environment or install it using environment.yml
install mrcfile and configparser using:

conda install -c conda-forge mrcfile

conda install configparser
 
To create dataset using weak phase model run ./generate_data.sh

This runs wp_dataset_generator.py using configs/parameters_generate_dataset.cfg file.

To modify the parameters of this dataset change the cfg file or create a new one and pass it to the wp_dataset_generator.py in command line


