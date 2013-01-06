#!/usr/bin/env python

# Plac bootstrap https://github.com/DarwinAwardWinner/python-script-template/blob/master/python-script.py
import plac, logging

# Export dependencies
import flickrapi, urllib, io, json, os.path
from config import api_key, api_secret, user_id as flickr_user_id

@plac.annotations(
    # arg=(helptext, kind, abbrev, type, choices, metavar)
    destination=("The directory to output the photos and metadata", "positional", None, str, None, "destination"),
    quiet=("Do not print informational messages.", "flag", "q"),
    fetchphotos=("Fetch the photos.", "flag", "f"),
    verbose=("Print debug messages that are probably only useful if something is going wrong.", "flag", "v"),
)
def main(destination, fetchphotos = False, quiet=False, verbose=False):
    """Backup a users photos """
    
    if quiet:
        logging.basicConfig(level=logging.WARN)
    elif verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Setup API and authenticate
    flickr = authenticate(flickrapi.FlickrAPI(api_key, api_secret))
    photos = {}

    logging.warn("Fetching photo metadata")
    
    for photo in flickr.walk(user_id=flickr_user_id, per_page=250, extras='description, url_o, tags, date_taken, views, original_format'):

        photos[photo.get('id')] = {
            'title': photo.get('title'),
            'description': photo.find('description').text,
            'file': '%s/%s.%s' % (destination, photo.get('id'), photo.get('originalformat')),
            'original_url': photo.get('url_o'),
            'width': photo.get('width_o'),
            'height': photo.get('height_o'),
            'date_taken': photo.get('datetaken'),
            'tags': photo.get('tags').split(),
            'views': photo.get('views'),
            'flickr_id': photo.get('id'),
        }
        
    
    logging.warn("Writing photo metadata")
    with io.open('%s/photos.json' % (destination), 'w+') as photos_file:
        photos_file.write(unicode(json.dumps(photos)))

    if fetchphotos:

        from multiprocessing import Pool
        pool = Pool(5)
        pool.map(fetch_image, photos.values())

def fetch_image(photo):
    if not os.path.isfile(photo['file']):
        logging.warn("Writing photo for: %s" % (photo.get('flickr_id')))
        urllib.urlretrieve(photo.get('original_url'), photo['file'])
    else:
        logging.warn("Skipping photo for: %s" % (photo.get('flickr_id')))

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
