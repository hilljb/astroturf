#!/usr/bin/python2

from __future__ import print_function

import requests
from requests_oauthlib import OAuth1

from urlparse import urlparse, urlunparse
from urllib import urlencode
from urllib import __version__ as urllib_version

import simplejson as json

import time
from datetime import datetime
import pytz

import sys

# import config (API keys) and settings
import astroturf_config


###################################################################################################
# Globals for time keeping                                                                        #
###################################################################################################

utc = pytz.utc


class RecentFollowers(object):
    """
    Class to query Twitter for 200 most recent followers of a user.
    """
    def __init__(self, user_id):
        """
        Initialize the class. Bring in and set config vars.
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

    def parse_time(self, this_time):
        """
        Parse a time in the form "Tue May 03 02:50:09 +0000 2016" into a timestamp.
        """
        dt = pytz.utc.localize(datetime.strptime(this_time, '%a %b %d %H:%M:%S +0000 %Y'))
        epoch = pytz.utc.localize(datetime.strptime('Thu Jan 01 00:00:00 +0000 1970','%a %b %d %H:%M:%S +0000 %Y'))
        timestamp = long((dt - epoch).total_seconds())
        return timestamp

    def find_age(self, user):
        """
        Adds age info to the user dict. How long has this user been on Twitter?
        """
        if 'created_at' in user:
            created_at_ts = self.parse_time(user['created_at'])
            user['created_at_ts'] = created_at_ts
            user['found_at'] = long(time.time())
            user['created_at_age'] = long(time.time() - created_at_ts)
        return user

    def get_user_id(self, user):
        """
        Returns the user id of the user in question. Used for uniqueness.
        """
        if 'id' in user:
            return long(user['id'])


if __name__ == "__main__":

    hillary_followers = RecentFollowers(user_id=1339835893)
    known_users = set()

    while True:
        # The data file to record these entries to
        received_data = '../../data/users.json'
        metrics_data = '../../data/metrics.json'
        f_p = open(received_data, 'a')
        g_p = open(metrics_data, 'a')

        # Save metrics on newly found users
        metrics = {
            'new_user_count': 0,
            'total_age': 0
        }
        ages = []

        # Get a list of the most recent 200 followers
        (resp_code, resp_data) = hillary_followers.get()

        # If the response code is 200, record the data
        if resp_code == 200:

            json_data = json.loads(resp_data)

            for user in json_data['users']:
                this_user_id = hillary_followers.get_user_id(user)

                if this_user_id not in known_users:
                    # record info about the user
                    known_users.add(this_user_id)
                    user = hillary_followers.find_age(user)
                    f_p.write("%s\n" % json.dumps(user))

                    # add user to metrics for this batch
                    metrics['new_user_count'] += 1
                    metrics['total_age'] += user['created_at_age']
                    ages.append(user['created_at_age'])

        else:
            print("response code: %s" % resp_code)
            print("response: %s" % resp_data)

        f_p.close()

        # get the median age
        if len(ages) > 0:
            ages.sort()
            median_age = ages[len(ages)/2]
        else:
            median_age = None

        # write metrics
        if metrics['new_user_count'] == 0:
            metrics['average_age'] = 0
        else:
            metrics['average_age'] = metrics['total_age'] / metrics['new_user_count']
        metrics['time'] = long(time.time())
        metrics['median_age'] = median_age
        g_p.write("%s\n" % json.dumps(metrics))
        g_p.close()

        # print to screen
        print(resp_code)
        print(metrics)
        print("\n")

        # Sleep for 60 seconds before getting new users
        time.sleep(60)
