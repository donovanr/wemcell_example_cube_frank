# How to use WESTPA and MCell together

## Install WESTPA and dependencies

Based on the instructions here:
https://github.com/westpa/westpa

### Install Anaconda (python and libraries):
- download the Anaconda install script
   - `curl -O "https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.2.0-Linux-x86_64.sh"`
- run the install script
   - `bash Anaconda-2.2.0-Linux-x86_64.sh`
- add anaconda to path in ~/.bashrc, if you didn't let the script do it for you:
   - `export PATH="${HOME}/anaconda/bin:$PATH"`
   - `source ~/.bashrc`
- make sure anaconda is up to date
   - `conda update conda`
   - `conda update anaconda`
- check to make sure anaconda python is now the default
   - `which python`
     - should be `~/anaconda/bin/python`

### Install WESTPA:
- get the current WESTPA
   - `git clone https://github.com/westpa/westpa.git`
- run the setup script
   - `./setup.sh`

## Install MCell

- download MCell: `http://mmbios.org/index.php/mcell-3-3`
- move it to server:
   - `scp mcell-3.3_x86_64.gz <user>@<server.address>:~/`
- on the server, move it somewhere sensible:
   - `mkdir ~/bin`
   - `mv mcell-3.3_x86_64.gz ~/bin`
- add ~/bin to path in ~/.bashrc:
   - `export PATH="${HOME}/bin:$PATH"`
   - `source ~/.bashrc`
- unzip the mcell download:
   - `gzip -d mcell-3.3_x86_64.gz`
- give it executable privileges:
   - `chmod +x mcell-3.3_x86_64`
- make an alias so our scripts don't break when if we upgrade mcell
   - `ln -s mcell-3.3_x86_64 mcell`
- which mcell should be `~/bin/mcell` and you should be able to get the mcell help screen by entering `mcell` in any directory

## If you are using OS X

These scripts use `sed` to edit data files inline, and the `sed` that comes with OS X is somewhat impaired in this regard.
The easiest way to fix the problem is to install gnu-sed with [homebrew](http://brew.sh/):
- `brew install gnu-sed`
- `ln -s /usr/local/bin/gsed /usr/local/bin/sed`

That last command will make it so that you use `gsed` everywhere `sed` is normally used.
I'm not aware of any serious drawbacks to this, but if you prefer not to do so, you can instead edit `runseg.sh` and change the single invocation of `sed` to `gsed`

## Clone this repository and run the simulation

- move to wherever you want to store this project
   - `git clone https://github.com/donovanr/wemcell_example_cube.git`
- change into the directory of the new project
   - `cd wemcell_example_cube`
- submit the job to the queue
   - `qsub submit_job.pbs`
- with the default settings, it should take 10 minutes to run the simulation.

## Plot output

I've included a very basic tool to plot the results of the simulation using only a terminal.

Once the simulation is done running,
- `cd ascii_plots`

Make sure we have th appropriate version of python loaded up:
- ./load_modules.sh

If you would like to look at the probability distribution of the progress coordinate (i.e bound receptors on the bottom of the cube) at a given iteration (say, iteration 50):
- `./ascii_plot.py --iter 50 --file ../west.h5`

If you would like to see that probability distribution evolve in time:
- `./ascii_movie.sh`


## Change simulation parameters

Most of the MCell parameters can be changed in `bstates/example_system_cube/Scene.WE.mdl`. 
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
   - `we_iters` in `bstates/example_system_cube/Scene.WE.mdl`
   - `west:propogation:max_total_iterations` in `west.cfg`

- number of times per weighted ensemble iteration to record data. `substeps` should be one less than `pcoord_len`.
   - `substeps` in `bstates/example_system_cube/Scene.WE.mdl`
   - `self.pcoord_len` in `system.py`

### WESTPA parameters

As usual, if you want to change the bins, and number of trajectories per bin, you can edit these settings in `system.py`.
