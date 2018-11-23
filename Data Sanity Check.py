import os
import shutil
import json

source_path = '/Users/tanmoy.sil/Pictures/Google Photos/'
destination_path = '/Users/tanmoy.sil/Downloads/Target/'
config_file_location = '/Users/tanmoy.sil/Downloads/Flickr/72157697558947470_9118eb201e2c_part1/albums.json'
unknown_album = '/Users/tanmoy.sil/Downloads/Target/NoAlbum/'

def find_file(name, path):
    # find file in given path (the first match)
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file:
                return os.path.join(root, file)
        for dir in dirs:
            res = find_file(name, path + dir)
            if res: return res


def move_file(src, dest):
    # copy file from source to destination
    try:
        shutil.move(src, dest)
    # eg. source and destination are the same file
    except shutil.Error as e:
        print('Error: {0}'.format(e))
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: {0}'.format(e.strerror))


# Find all files that exists in source dir
sFiles = []
for root, dirs, files in os.walk(source_path):
    for file in files:
        if file != '.DS_Store':
            sFiles.append(os.path.join(root, file))
    for dir in dirs:
        for root1, dirs1, files1 in os.walk(source_path + dir):
            for file1 in files1:
                if file1 != '.DS_Store':
                    sFiles.append(os.path.join(root1, file1))
for file in sFiles:
    d, f = os.path.split(file)
    s_path = find_file(f, destination_path)
    if s_path:
        os.remove(file)
        # print("Delete ", file)
    else:
        move_file(file, unknown_album)
        print("Cant found ", file)

# print("\n".join(sFiles))
#
# if not os.path.exists(destination_path):
#     os.mkdir(destination_path)
#
# if config_file_location:
#     with open(config_file_location, 'r') as f:
#         datastore = json.load(f)
#
#     for album in datastore['albums']:
#         path_dir = destination_path + album['title'].strip()
#         if not os.path.exists(path_dir):
#             os.mkdir(path_dir)
#
#         for photo in album['photos']:
#             s_path = find_file(photo, source_path)
#             if s_path: copy_file(s_path, path_dir)
#             print(s_path)
#             # break
#
#
