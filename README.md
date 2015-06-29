# How to use WESTPA and MCell together

This repository conatins everything you should need to run an MCell simualtion using WESTPA on frank.

The environment variables are set specifically to work on frank.sam.pitt.edu.
If you would like to install and run on a different (generic) system, see the instructions [here](https://github.com/donovanr/wemcell_example_cube).

## Clone this repository and run the simulation

- In your home directory on frank, or wherever you want to store this directory,
   - `git clone https://github.com/donovanr/wemcell_example_cube_frank.git`
- change into the directory of the new project
   - `cd wemcell_example_cube_frank`
- submit the job to the queue
   - `qsub submit_job.pbs`
- with the default settings, it should take 10 minutes to run the simulation.

## Plot output

I've included a very basic tool to plot the results of the simulation using only a terminal.

Once the simulation is done running,
- `cd ascii_plots`

Make sure we have the appropriate version of python loaded up:
- `./load_modules.sh`

If you would like to look at the probability distribution of the progress coordinate (i.e bound receptors on the bottom of the cube) at a given iteration (say, iteration 50):
- `./ascii_plot.py --iter 50 --file ../west.h5`

If you would like to see that probability distribution evolve in time:
- `./ascii_movie.sh`


## Change simulation parameters

Most of the MCell parameters can be changed in `bstates/example_system_cube_frank/Scene.WE.mdl`. 
Most of the WESTPA parameters can be changed in `system.py` and `west.cfg`.

### Extra parameters specific to MCell

There are three parameters in `runseg.sh` that need to be set for MCell to properly run.
They are:
- `MCELL`
   - the version of mcell we are using
- `MODEL_NAME`
   - the name of the directory all the model files live in 
- `OBSERVABLE1`
   - observable we are using as our (1st) progress coordinate

Note that there are plenty of other parameters internal to MCell that can be set, these are just the extra ones needed for MCell and WESTPA to properly continue trajectories.

### Parameters that need to be changed in two places

Changing some simulation parameters can be a little fussy, since you have to set the new value in two places.
This is becasue both MCell and WESTPA independently need to know, e.g. how many iterations to run.

The variables that need to be changed in two places are listed below:

- number of weighted ensemble iterations to run. The following parameters should be the same:
   - `we_iters` in `bstates/example_system_cube_frank/Scene.WE.mdl`
   - `west:propogation:max_total_iterations` in `west.cfg`

- number of times per weighted ensemble iteration to record data. `substeps` should be one less than `pcoord_len`.
   - `substeps` in `bstates/example_system_cube_frank/Scene.WE.mdl`
   - `self.pcoord_len` in `system.py`

### WESTPA parameters

As usual, if you want to change the bins, and number of trajectories per bin, you can edit these settings in `system.py`.
