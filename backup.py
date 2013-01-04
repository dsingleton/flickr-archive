#!/usr/bin/env python

# Plac bootstrap https://github.com/DarwinAwardWinner/python-script-template/blob/master/python-script.py
import plac, logging

# Export dependencies
import flickrapi, urllib
from config import api_key, api_secret, user_id as flickr_user_id


@plac.annotations(
    # arg=(helptext, kind, abbrev, type, choices, metavar)
    destination=("The directory to output the photos and metadata", "positional", None, str, None, "destination"),
    quiet=("Do not print informational messages.", "flag", "q"),
    verbose=("Print debug messages that are probably only useful if something is going wrong.", "flag", "v"),
)
def main(destination, quiet=False, verbose=False):
    """Backup a users photos """
    if quiet:
        logging.basicConfig(level=logging.WARN)
    elif verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Setup API and authenticate
    flickr = authenticate(flickrapi.FlickrAPI(api_key, api_secret))
    
    for photo in flickr.walk(user_id=flickr_user_id, per_page=10, extras='original_format, url_o, date_taken'):
        print photo.get('id')
        # process_photo(destination, photo)

def process_photo(destination, photo):
    localfile = '%s/%s - %s.%s' % (destination, photo.get('id'), photo.get('title', '').replace('/', ':'), photo.get('originalformat'))
    urllib.urlretrieve(photo.get('url_o'), localfile)

def authenticate(flickr):
    """"Super simple Authentication

    http://stuvel.eu/media/flickrapi-docs/documentation/#authentication"""

    (token, frob) = flickr.get_token_part_one(perms='write')
    if not token:
        raw_input("Press ENTER after you authorized this program")

    flickr.get_token_part_two((token, frob))

    return flickr

if __name__=="__main__":
    plac.call(main)
