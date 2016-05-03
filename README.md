# Astroturf

Are the candidates astroturfing on Twitter?

## Setup

The `setup` folder contains a Bash script. Assuming you have [Anaconda](https://www.continuum.io/downloads)
installed, you can simply run this script to set up your conda environment.

To activate the conda environment:
```
source activate astroturf
```

Place your Twitter API keys in the `src/python` directory in a file named `astroturf_config.py`. The file
should look like the following.

```
credentials = {
    'consumer_key': 'yourconsumerkey',
    'consumer_secret': 'yourconsumersecret',
    'access_token_key': 'youraccesstokenkey',
    'access_token_secret': 'youraccesstokensecret'}
```

You probably want to `screen` the script itself, as it makes an API call every 60 seconds.

## Running the script

With the astroturf conda environment activated, simply run the script with the id of the user
you wish to track. In this case, we're using Hillary Clinton: 1339835893

```
python get_followers.py 1339835893
```

The resulting data and response codes will be placed in the `astroturf/data` directory.
