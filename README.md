# Atrial-fib-sim

This package can be used to simulate atrial fibrillation. The point of the project was to trigger atrial fibrillation to the investigate whether randomly induced ablation of selected cells would be an available method for ammending this issue. I have yet to find any method that is less destructive than it unfortunately currently is.

There are several parameters one can play around with. The run.py file is where parameters and variables are set and is intended as the main interface. This package is open source and subject to the GNU license agreement. If you like this package or have suggestions for changes please let me know. 

## Example and parameter specification found in run.py

- tmax = 1000     says itself
- D = 250         array dimensions DxD

### AF = i._init_(D,tmax,
- t_r=15,                 Sets the length of the pulse i.e. the lagg time until at cell can be reexited\\
- v=0.9,                  probability of breaking a random link. not currently in use.
- threshold=0.9,          Probability of killing a cell a value 0f .9 kills 90 percent of cells according to a normal distribution\\
- limit=10,               boundary condition. a value of 10 means all conditional arguments of killing and destroying verticle links happen within this boundary
- dys_link_prob=0.085,    probability of destroying a verticle link
- dys_cell_prob=0.2,      Probability of a cell being set to dysfunctional
- pulse_time = 50)        Sets the time inbetween pulses

### AF.init(
- break_links=True,            argument that passes whether links should be broken
- treatment=True,              runs the simulation again including treatming i.e. randomized cell death
- skip_first_loop = False)     intended to skip the first simulation without cell ablation. triggering fibrillation is hard, so each simulation prior to treatment is stored in a array.npy so verious methods of cell ablation may be tried.

- vid1 = vid.video() 
- vid1.side_by_side(fps=1.25)


## Packages need
- Numpy
- Opencv
- matplotlib
- imageio

## Litterature
The code was reverse engineered and the theory based upon the article "Still looking for the specific article will put citation as soon as it is found"

### Collaboration
This was my first large coding project and there is much work to be done on the optimization of run time. Reducing the amount of for loops etc and general quality of life improvements would be much appreciated. Please contact me with any suggestions towards the project
