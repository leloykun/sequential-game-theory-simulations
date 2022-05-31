# Simulations of Sequential Games with Multi-agent Reinforcement Learning

[![Pisay](https://img.shields.io/badge/pshs-evc-blue.svg)](http://evc.pshs.edu.ph/)
[![Build Status](https://travis-ci.org/leloykun/socialsims.svg?branch=master)](https://travis-ci.org/leloykun/socialsims)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ee723a36e510464aab4bd4fbe8ef1779)](https://www.codacy.com/app/leloykun/socialsims?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=leloykun/socialsims&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ee723a36e510464aab4bd4fbe8ef1779)](https://www.codacy.com/app/leloykun/socialsims?utm_source=github.com&utm_medium=referral&utm_content=leloykun/socialsims&utm_campaign=Badge_Coverage)

Simulations on the collective behavior of reinforcement learning agents

<img src="https://github.com/leloykun/socialsims/blob/master/data/plots/regression/degree1/frame315.jpeg" width="45%" height="45%"> <img src="https://github.com/leloykun/socialsims/blob/master/data/plots/regression/degree2/frame315.jpeg" width="45%" height="45%"> 
<img src="https://github.com/leloykun/socialsims/blob/master/data/plots/regression/degree3/frame315.jpeg" width="45%" height="45%"> <img src="https://github.com/leloykun/socialsims/blob/master/data/plots/regression/logistic/frame315.jpeg" width="45%" height="45%">

NOTE: This project is not finished yet. See the older version [here](https://github.com/leloykun/cultural-evolution/tree/master/miscSims).

## Gettting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Language
[Python 3.x](https://www.python.org/downloads/) (preferably [python 3.5](https://www.python.org/downloads/release/python-350/)) 

### Installation
Download or clone the repository using the big green button on the upper-right corner of the page or by using git:
```bash
git clone git://github.com/leloykun/socialsims.git
```
or
```bash
git clone https://github.com/leloykun/socialsims.git
```

### Libraries
Install the required libraries with pip:
``` bash
pip install -r requirements.txt
```
or
``` bash
pip3 install -r requirements.txt
```

## Running the simulations
You can run all of the simulations in one go with:
```bash
python main.py
```
The raw data for each simulation can be found in `data/raw/[name of simulation]`

### Testing
Just run
```bash
pytest
```

### Turning on the visuals
The visuals are turned off by default to speed up the simulations.

To turn them on, simply uncomment the line with `env.show()` in the source code of each simulation:
```python
# env.show()
env.show()
```

This is *NOT* recommended.

TODO: centralize this option

### Running the simulations individually
You can comment out the simulations in `src/sims/list.txt` to exclude them from being run by `portal.py`. For example, with the following, only simulation `cat-mouse` would be run with parameters `100 10 10` as `[runs] [trials] [steps]`.
```txt
# cat-mouse [runs] [trials] [steps]
cat-mouse 10 100 10

# cat-mouse-cheese [runs] [timesteps] [interval]
# cat-mouse-cheese 10 10000 100

# simple-migration [runs] [timesteps] [temp_powers]
# simple-migration 10 10000 5

# route-choice [runs] [timesteps] [num_drivers] [[road capacities]]
# route-choice 10 1000 100 10 20 30 40

# migration [runs] [timesteps] [num_mice]
# migration 1 100000 3
```

TODO: fix this

## Data Analysis
TODO

## Details
TODO

TODO move this part to 'wiki'

### Reinforcement Learning
TODO

### Simulations on Specialization
TODO

### Simulations on Migration
TODO

### Simulations on Cooperation
TODO

## Results and Discussion
TODO

TODO use seaborn facet grid to graph data

## Developer
- Franz Louis Cesista
- Grade 12 student from Philippine Science High School - Eastern Visayas Campus
- Machine Learning enthusiast
