import os
import shutil
import json

source_path = '/Users/tanmoy.sil/Pictures/Google Photos/'
destination_path = '/Users/tanmoy.sil/Downloads/Target/'
config_file_location = '/Users/tanmoy.sil/Downloads/Flickr/72157697558947470_9118eb201e2c_part1/albums.json'

def find_file(name, path):
    # find file in given path (the first match)
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file:
                return os.path.join(root, file)
        for dir in dirs:
            res = find_file(name, path + dir)
            if res: return res


def copy_file(src, dest):
    # copy file from source to destination
    try:
        shutil.move(src, dest)
    # eg. source and destination are the same file
    except shutil.Error as e:
        print('Error: {0}'.format(e))
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: {0}'.format(e.strerror))



if not os.path.exists(destination_path):
    os.mkdir(destination_path)

if config_file_location:
    with open(config_file_location, 'r') as f:
        datastore = json.load(f)

    for album in datastore['albums']:
        path_dir = destination_path + album['title'].strip()
        if not os.path.exists(path_dir):
            os.mkdir(path_dir)

        for photo in album['photos']:
            s_path = find_file(photo, source_path)
            if s_path: copy_file(s_path, path_dir)
            print(s_path)
            # break


