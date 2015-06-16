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
   - source ~/.bashrc
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

## Clone this repository and run the simulation

- move to wherever you wan to store this project
   - `git clone https://github.com/donovanr/wemcell_example_cube.git`
- change into the directory of the new project
   - `cd wemcell_example_cube`
- set the environment
   - `./env.sh`
- intialize the WE simulation
   - `./init.sh`
- run the WE simulation
   - `./run.sh`
