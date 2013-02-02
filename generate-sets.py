#!/usr/bin/env python

import sys, io, os, json

def generate_sets(photos_directory):
    with io.open('%s/photos.json' % (photos_directory), 'r') as photos_file:
        photos = json.loads(photos_file.read())
        photos_map = dict((photo.get('flickr_id'), photo) for photo in photos)

    with io.open('%s/sets.json' % (photos_directory), 'r') as photosets_file:
        photosets = json.loads(photosets_file.read())

        photosets_directory = '%s/Sets' % photos_directory

        try:
            os.stat(photosets_directory)
        except:
            os.makedirs(photosets_directory)


        for photoset in photosets:
            
            photoset_directory = '%s/%s' % (photosets_directory, photoset['title'])
            
            try:
                os.stat(photoset_directory)
            except:
                os.makedirs(photoset_directory)

            for photo_id in photoset.get('photos'):
                photo_name = '%s/%s (%s).%s' % (photoset_directory, photos_map[photo_id].get('title'), photo_id, 'jpg')
                photo_name = '%s/%s.%s' % (photoset_directory, photo_id, 'jpg')
                
                try:
                    os.symlink(photos_map[photo_id].get('file'), photo_name)
                except OSError:
                    print "SKIPPING: %s" % photo_name


if __name__=="__main__":
    try:
        photos_directory = sys.argv[1]
    except IndexError:
        photos_directory = '.'
    
    generate_sets(photos_directory)
