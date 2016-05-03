#!/bin/bash

source activate astroturf
conda env export > astroturf.yml
source deactivate
