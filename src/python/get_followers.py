#!/usr/bin/python2

from __future__ import print_function

import requests
from requests_oauthlib import OAuth1

from urlparse import urlparse, urlunparse
from urllib import urlencode
from urllib import __version__ as urllib_version

import simplejson as json

import time
import sys

# import config (API keys) and settings
import astroturf_config


class RecentFollowers(object):
    """
    
    """
    def __init__(self, user_id):
        """
        
        """
        self._user_agent = 'Python-urllib/%s' % urllib_version
        self._url = 'https://api.twitter.com/1.1/followers/list.json'
        self._oauth = OAuth1(
            astroturf_config.credentials['consumer_key'],
            astroturf_config.credentials['consumer_secret'],
            astroturf_config.credentials['access_token_key'],
            astroturf_config.credentials['access_token_secret'])
        self._parameters = {
            'user_id': user_id,
            'count': int(200),
            'skip_status': False,
            'include_user_entities': True,
            'cursor': -1
        }

    def get(self):
        """
        Issue the get request to the Twitter API and parse the response.
        """
        # Parse the URL into components        
        (scheme, netloc, path, params, query, fragment) = urlparse(self._url)
        # Use parameters to encode request and add to URL
        encoded_params = urlencode(
            dict(
                [(k, str(v).encode('utf-8')) for k, v in list(self._parameters.items())]
            )
        )

        if query:
            query += '&' + encoded_params
        else:
            query = encoded_params
        # Form the URL
        url = urlunparse((scheme, netloc, path, params, query, fragment))

        # Issue the request
        resp = requests.get(url, auth=self._oauth)

        # Get the response code
        resp_code = resp.status_code

        # Get the data
        resp_data = resp.content.decode('utf-8')

        # Return a tuple of response code and data
        return (resp_code, resp_data)


hillary_followers = RecentFollowers(user_id=1339835893)
hillary_followers.get()
print('done')
