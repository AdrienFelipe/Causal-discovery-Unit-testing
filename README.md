# Causal discovery Unit testing

This project aims to provide a framework to execute **structural equation model** searches as **unit tests**.     
It gives access to a wide range of causal relations by allowing the creation of functional equations models from its dataset generator.

## Docker
The environment is self contained by enjoying the power of docker. All dependencies will be installed in an anaconda virtual environment inside a docker container.    
Run `make start` to install and launch the container. It will take a few minutes only the first time to install all packages. 

Once installed run `make run` to launch causal explorations on a few datasets to validate everything was properly installed.   

## Configuration
Datasets and algorithms executed by the `run`command are defined in the `src/ui/config.py` configuration file.

## Pre-configured datasets
A list of datasets are available in the folder `src/datasets/` grouped by type:
- *unit*: as unitary datasets
- *causality*: as a range of causal relation types
- *integration*: as simulated real case datasets

## Jupyter notebook
To execute a jupyter notebook from the container run `make jupyter notebook`    
Check the makefile for a list of all available commands.

## Disclaimer
This is a master degree final project, and it is not meant to be production ready.    
It was only tested on a linux environment, and some commands might not work on windows.
