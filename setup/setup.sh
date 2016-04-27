#!/bin/bash

# Sets up the conda environment
# Requires anaconda/conda: https://www.continuum.io/downloads

set -x

# Determine if the environment already exists
ASTROTURF_EXISTS="$(conda env list | grep "^astroturf" | grep -c "astroturf$")"
echo "ASTROTURF_EXISTS=$ASTROTURF_EXISTS"

# Install it if it doesn't exist
if [[ "$ASTROTURF_EXISTS" -eq "0" ]]; then
    echo "creating environment"
    conda env create -f astroturf.yml
else
    echo "environment already exists"
fi
