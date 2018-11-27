import os
import shutil

source_path = '/Users/tanmoy.sil/Pictures/Google Photos/'
destination_path = '/Users/tanmoy.sil/Downloads/Target/'
unknown_album = '/Users/tanmoy.sil/Downloads/Target/NoAlbum/'

# This is a sanity checking program, if we have a file in Google Uploader and not exists in Target directory, that means
# it is un-categorized (not part of any albums), we need to put this in an Unknown Album.


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


def main():
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


if __name__ == '__main__':
    main()

