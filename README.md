# Social Simulations with Reinforcement Learning
Simulations on specialization, migration, and cooperation

<img src="https://github.com/leloykun/socialsims/blob/master/docs/experiments/4/1/plotloop.gif" alt="alt text" width="45%" height="45%"> <img src="https://github.com/leloykun/socialsims/blob/master/docs/experiments/6/1plot-both.png" alt="alt text" width="45%" height="45%">

NOTE: This project is not finished yet. See the older version [here](https://github.com/leloykun/cultural-evolution/tree/master/miscSims). See deprecated simulations [here](https://github.com/leloykun/socialsims/tree/master/docs/experiments).

## Gettting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
[Python 3.x](https://www.python.org/downloads/) (preferably [python 3.6](https://www.python.org/downloads/release/python-360/)) are needed to run the tests.

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
![](https://github.com/leloykun/socialsims/blob/master/docs/env_show.png)

This is NOT recommended.

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
You can comment out the simulations in `list.txt` to exclude them from being run by `portal.py`. For example, with the following, only simulation `cat-mouse` would be run with parameters `100 10 10` (more on this later).
```txt
cat-mouse 100 10 10
# cat-mouse-cheese 10000 100 10
# simple-migration 10000 10 5
```

TODO: explain what the parameters are about

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
TODO use sklearn to analyze agent performance vs. qlearning parameters 
(tho not sure wether I'll use logistic regression then graph the results or create a mathematical model with linear regression)
TODO use seaborn facet grid to graph data
TODO readd going-to-obstacles option

## Developer
- Franz Louis Cesista
- Grade 12 student from Philippine Science High School - Eastern Visayas Campus
- Machine Learning enthusiast
