# HMC eMPRess Codebase for Spring 2020 Research

## Overview
eMPRess supports the following functionality:
* DTL Reconciliation - `reconcile`
* Costscape - `costscape`
* Pair-distance Histogram - `histogram`
* Cluster MPR - `clumpr`

## Installing Dependencies
The package uses [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) to install dependencies. Please refer to the Pipenv website on how to install pipenv.

On the command line, run:
```bash
pipenv install # create virtual environment and install dependencies
pipenv shell # enter the virtual environment with dependencies installed
```
Every time you restart the terminal, make sure you run `pipenv shell` before running empress script.

## Running eMPRess

On the command line, the structure of the inputs are:    
* `python empress.py -fn <path to tree data file> <functionality>`

For example, to run Costscape with default parameters, you run:
* `python empress.py -fn examples/heliconius.newick costscape`

For specific parameters of each functionality, consult the list below:

## List of Parameters
Note: value in parenthesis denotes default value, asterisk denotes boolean flags
### Costscape
* `-dl` : Duplication low value (1)
* `-dh` : Duplication high value (5)
* `-tl` : Transfer low value (1)
* `-th` : Transfer high value (5)
* `--outfile` : Name of output file. Must end in .pdf ("")
* `--log` : Set graph to log scale*
* `--display` : Display graph to screen*


For example, the following example runs Costscape with duplication low value of 0.5, duplication high value of 10, transfer low value of 0.5, 
and transfer high value of 10, that saves to a file called `foo.pdf` display it in log scale.
* `python empress.py -fn examples/heliconius.newick costscape -tl 0.5 -th 10 -dl 0.5 -dh 10 --outfile costscape-example-img.pdf --log`

### DTL Reconciliation
* `-d` : Duplication cost (2)
* `-t` : Transfer cost (3)
* `-l` : Lost cost (1)

For example, to run DTL Reconciliation with duplication cost of 4, transfer cost of 2 and lost cost of 0, you run
* `python empress.py -fn examples/heliconius.newick reconcile -d 4 -t 2 -l 0`

### Pair distance Histogram
* `-d` : Duplication cost (2)
* `-t` : Transfer cost (3)
* `-l` : Lost cost (1)
* `--histogram` : Name of output file. If no filename is provided, outputs to a filename based on the input tree data file
* `--xnorm` : Normalize the x-axis so that the distances range between 0 and 1*
* `--ynorm` : Normalize the y-axis so that the distances range between 0 and 1*
* `--omit-zeros` : Omit the zero column of the histogram, which will always be the total number of reconciliations*
* `--cumulative` : Make the histogram cumulative*
* `--csv` : Output the histogram as a .csv file at the path provided. If no filename is provided, outputs to a filename based on the input tree data file*
* `--stats` : Output statistics including the total number of MPRs, the diameter of MPR-space, and the average distance between MPRs*
* `--time` : Time the diameter algorithm*

For example, to run Pair-distance Histogram that outputs a csv file at `foo.csv`, outputs a histogram to `bar.pdf` and normalizes the y-axis, you run
* `python empress.py -fn examples/heliconius.newick histogram --csv foo.csv --histogram bar.pdf --ynorm`

### Cluster MPR
* `-d` : Duplication cost (2)
* `-t` : Transfer cost (3)
* `-l` : Lost cost (1)
* `-k` : Number of clusters
* `--median` : Print out medians of each cluster
* `--depth` : How far down the graph to consider event splits
* `--nmprs` : How many MPRs to consider
* `--pdv-vis` : Visualize the resulting clusters using the PDV*
* `--support-vis` : Visualize the resulting clusters using a histogram of the event supports*
* `--pdv` : Use the weighted average distance to evaluate clusters*
* `--support` : Use the weighted average event support to evaluate clusters*

For example, to run Cluster MPR that prints out the medians of each cluster with 4 MPRs using the weighted average event support, you run 
* `python empress.py -fn examples/heliconius.newick clumpr --median --nmprs 4 --support`