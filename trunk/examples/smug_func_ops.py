#!/bin/python

''' This example will return the URL of a random image from a users gallery'''
import smugmugapi as SI
import sys
import logging
import random
import urllib
import os
from optparse import OptionParser

def rotate_image_45 (sapi, session_id, image_id):
    result = sapi.images_rotate(SessionID=session_id, ImageID=image_id, Degrees = "45")
    return 

def upload_image (sapi, session_id, album_id, file_name):
    result = sapi.upload(file_name, SessionID=session_id, AlbumID=album_id)
    return 

def get_albums (sapi, session_id, nick):
    result = sapi.users_getTree(SessionID=session_id, NickName=nick)
    return 

def get_random_image (sapi, session_id):
    result = sapi.albums_get(SessionID=session_id)

    num_albums = len (result.Albums[0].Album)
    album_id = result.Albums[0].Album[random.randint(0,num_albums -1 )]["id"]

    result=sapi.images_get (SessionID=session_id, AlbumID=album_id)

    num_images = len(result.Images[0].Image)
    image_id = result.Images[0].Image[random.randint(0,num_images -1)]["id"]

    result=sapi.images_getURLs (SessionID=session_id, ImageID=image_id)

    large_url = result.Image[0]["LargeURL"]

    return large_url

def get_most_pop_album (sapi, session_id):
    result = sapi.albums_get(SessionID=session_id)


    album_list = result.Albums[0].Album
    num_albums = len (album_list)
    album_stats={}

    for album in album_list:
        result=sapi.albums_getStats (SessionID=session_id, AlbumID=album["id"], Month="1", Year="2007")
        album_stats[album["id"]] = int(result.Album[0]["Medium"])

    rev_items = [(v, k) for k, v in album_stats.items()]
    rev_items.sort()
    print rev_items
    print "Most popular album --->", rev_items[0][1]
    return rev_items[0][1]

def get_album_details (sapi, session_id, album_id):
    result=sapi.albums_getInfo (SessionID=session_id, AlbumID=album_id)
    return result.Album[0].Title


def get_image (sapi, session_id, image_id):
    result=sapi.images_getURLs (SessionID=session_id, ImageID=image_id)
    tiny_url = result.Image[0]["TinyURL"]
    return result

def download_image (sapi, session_id, image_id, path):
    result=sapi.images_getURLs (SessionID=session_id, ImageID=image_id)
    tiny_url = result.Image[0]["TinyURL"]

    urllib.urlretrieve (tiny_url, os.path.join(path, image_id + "-Ti.jpg"))
    

def download_album (sapi, session_id, album_id, path):
    """ download a complete album """
    result = sapi.albums_get(SessionID=session_id)

    result=sapi.images_get (SessionID=session_id, AlbumID=album_id)
    num_images = len(result.Images[0].Image)
    image_list = result.Images[0].Image

    for image in image_list:
        download_image (sapi, session_id, image["id"], path)

    return None

def user_login (sapi, email, password):
    ''' create a session for the specified user'''
    result=sapi.login_withPassword (EmailAddress = email, Password = password)
    session_id = result.Login[0].Session[0]["id"]
    return session_id

def anon_login (sapi):
    ''' create a session for the specified user'''
    result=sapi.login_anonymously ()
    session_id = result.Login[0].Session[0]["id"]
    print session_id
    return session_id

def init_parser ():

    # python smugmug_ops.py -e EMAIL -p PASSWORD -m upload_image -a ALBUMID -f IMAGEPATH
    # python smugmug_ops.py -e EMAIL -p PASSWORD -m random_image -d
    # python smugmug_ops.py -e EMAIL -p PASSWORD -m get_albums -n NICK -d

    parser = OptionParser(usage="%prog -m MODE [-e EMAIL] [-p PASSWORD] [-n NICKNAME] [-o OUTPUTDIR]  [-d] [-a ALBUMID] [-i IMAGEID] [-f IMAGEPATH]")

    parser.add_option("-e", "--email",
                      action="store", type="string", dest="email",
                      help="XYZ")
    parser.add_option("-p", "--password",
                      action="store", type="string", dest="password",
                      help="XYZ")

    parser.add_option("-m", "--mode",
                      action="store", type="choice", dest="mode",
                      choices=["random_image", "pop_album", "download_album_tiny", "get_albums", "upload_image", "rotate_image_45", "find_image", "album_details"],
                      help="Specify one mode: random_image, pop_album, download_album_tiny, get_albums")

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enable debugging [default: %default]")

    parser.add_option("-a", "--albumid",
                      action="store", type="int", dest="album_id",
                      help="Specify album id")

    parser.add_option("-i", "--imageid",
                      action="store", type="int", dest="image_id",
                      help="Specify image id")

    parser.add_option("-f", "--file",
                      action="store", type="string", dest="file_name",
                      help="Specify file (absolute path required)")

    parser.add_option("-o", "--output",
                      action="store", type="string", dest="output",
                      help="Output directory")

    parser.add_option("-n", "--nick",
                      action="store", type="string", dest="nick",
                      help="Nickname (only to be used with mode get_albums)")


    return parser


def main ():
    smugmug_api_key = "29qIYnAB9zHcIhmrqhZ7yK7sPsdfoV0e"  # API key

    sapi = SI.SmugMugAPI (smugmug_api_key)
    parser = init_parser()
    (options, args) = parser.parse_args()
    if options.debug:
        SI.set_log_level(logging.DEBUG)

    session_id = user_login (sapi, options.email, options.password)
    #session_id = anon_login (sapi) # add command line option to support anon logins

    if options.mode == "random_image": 
        print get_random_image(sapi, session_id)
    elif options.mode == "pop_album": 
        print get_most_pop_album(sapi, session_id)
    elif options.mode == "download_album_tiny": 
        print download_album(sapi, session_id, options.album_id, options.output)
    elif options.mode == "get_albums": 
        print get_albums(sapi, session_id, options.nick)
    elif options.mode == "upload_image": 
        print upload_image(sapi, session_id, options.album_id, options.file_name)
    elif options.mode == "rotate_image_45": 
        print rotate_image_45(sapi, session_id, options.image_id)
    elif options.mode == "find_image": 
        print get_image (sapi, session_id, options.image_id)
    elif options.mode == "album_details": 
        print get_album_details (sapi, session_id, options.album_id)

    return

# run main if we're not being imported:
if __name__ == "__main__":
    main()


