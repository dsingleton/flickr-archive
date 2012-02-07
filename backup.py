#!/usr/bin/python
import flickrapi, urllib, config, sys

flickr = flickrapi.FlickrAPI(config.api_key, config.api_secret)
flickr.token.path = '.tokens'

dest = sys.argv[1]

# Super simple Authentication - http://stuvel.eu/media/flickrapi-docs/documentation/#authentication
(token, frob) = flickr.get_token_part_one(perms='write')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

def process_photo(photo):
    localfile = '%s/%s - %s.%s' % (dest, photo.get('id'), photo.get('title', '').replace('/', ':'), photo.get('originalformat'))
    urllib.urlretrieve(photo.get('url_o'), localfile)

for photo in flickr.walk(user_id=config.user_id, per_page=10, extras='original_format, url_o, date_taken'):
    process_photo(photo)
    
