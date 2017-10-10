# Social Simulations with Reinforcement Learning

![Pisay](https://img.shields.io/badge/pshs-evc-blue.svg)
[![Build Status](https://travis-ci.org/leloykun/socialsims.svg?branch=master)](https://travis-ci.org/leloykun/socialsims)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ee723a36e510464aab4bd4fbe8ef1779)](https://www.codacy.com/app/leloykun/socialsims?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=leloykun/socialsims&amp;utm_campaign=Badge_Grade)

Simulations on specialization, migration, and cooperation

<img src="https://github.com/leloykun/socialsims/blob/master/docs/experiments/4/1/plotloop.gif" alt="alt text" width="45%" height="45%"> <img src="https://github.com/leloykun/socialsims/blob/master/docs/experiments/6/1plot-both.png" alt="alt text" width="45%" height="45%">

NOTE: This project is not finished yet. See the older version [here](https://github.com/leloykun/cultural-evolution/tree/master/miscSims). See deprecated simulations [here](https://github.com/leloykun/socialsims/tree/master/docs/experiments).

## Gettting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
[Python 3.x](https://www.python.org/downloads/) (preferably [python 3.5](https://www.python.org/downloads/release/python-350/)) is needed to run the tests.

The following python libraries must also be installed:
- [matplotlib](https://matplotlib.org/)
- [pygame](https://www.pygame.org/news)
- [numpy](http://www.numpy.org/)

This can be done by running the following in the command line:
```bash
pip install matplotlib pygame numpy
```
or:
```bash
pip3 install matplotlib pygame numpy
```
Note that this project has only been tested on windows 7

### Installing
Download or clone the repository to your prefered directory using the big green button on the upper-right corner of the page

or by using git:
```
git clone git://github.com/leloykun/socialsims.git
```
or
```
git clone https://github.com/leloykun/socialsims.git
```
And you're now ready to run the simulations!

## Running the simulations
You can run all of the simulations in one go with:
```bash
python portal.py
```
The raw data for each simulation can then be found in `sims/[name-of-simulation]/data/`

TODO: add better examples

### Turning on visuals
The visuals are hidden by default. This is to speed up the run times of the simulations.

If you want to turn turn them on, simply uncomment the line with `env.show()` in the source code of each simulation:
```python
# env.show()
env.show()
```

This is *NOT* recommended.

TODO: centralize this option

### Data visualization
For each simulation, go to the directory of its data and run the following in the command line:
```bash
python data_visualizer.py
```
The graphs would then be automatically generated for you.

Additionally, `data_visualizer.py` can easily be modified when needed.

TODO: centralize data visualization

### Running the simulations individually
You can comment out the simulations in `list.txt` to exclude them from being run by `portal.py`. For example, with the following, only simulation `cat-mouse` would be run with parameters `100 10 10` as `[runs] [trials] [steps]`.
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

### Running the tests
```bash
pytest tests/
```

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
