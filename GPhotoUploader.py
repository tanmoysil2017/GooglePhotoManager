import os
import shutil
import httplib2
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests


folder = '/Users/tanmoy.sil/Downloads/Test/'
archive_path = '/Users/tanmoy.sil/Downloads/Archive/'
error_path = '/Users/tanmoy.sil/Downloads/Error/'

# This program upload all photos from folder and put it under an album named folder name.
# In success it archives the pictures in archive_path, otherwise error_path


def upload(service, file):
    try:
        f = open(file, 'rb').read();

        url = 'https://photoslibrary.googleapis.com/v1/uploads'
        headers = {
            'Authorization': "Bearer " + service._http.request.credentials.access_token,
            'Content-Type': 'application/octet-stream',
            'X-Goog-Upload-File-Name': file,
            'X-Goog-Upload-Protocol': "raw",
        }

        r = requests.post(url, data=f, headers=headers)
        return r.content

    except:
        move_file(file, error_path)


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


def moveto_archive(file_path, file_dir):
    if not os.path.exists(archive_path + file_dir):
        os.mkdir(archive_path + file_dir)
    move_file(file_path, archive_path + file_dir)


def get_all_albums(service, http, ):
    ret_map = {}
    request = service.albums().list()
    while request is not None:
        albums_in_photos = request.execute(http=http)
        if 'albums' in albums_in_photos:
            for album_in_photos in albums_in_photos['albums']:
                ret_map[str(album_in_photos['title']).strip()] = album_in_photos['id']

        request = service.albums().list_next(request, albums_in_photos)

    return ret_map


def main():
    # Get Authentication token
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    # Create HTTP and Service
    http = httplib2.Http()
    http = creds.authorize(http)
    service = build('photoslibrary', 'v1', http=creds.authorize(Http()))

    # Get list of existing Albums (we don't want to create new album if it already exists)
    map_albums = get_all_albums(service, http)

    # Read all the image files
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            album_name = dir.strip()
            album_id = ''
            print ("Album ", album_name)

            # Get the Album id, from folder name, or create a new one - if needed
            if album_name in map_albums:
                album_id = map_albums[album_name]
            else:
                # Create an Album
                d = {
                    "album": {
                        "title": album_name
                    }
                }
                album = service.albums().create(body=d).execute(http=http)
                map_albums[album_name] = album['id']
                album_id = album['id']

            # Scan for image files in the Album Folder
            for root1, dir1, files1 in os.walk(folder+dir):
                for f in files1:
                    image_file = folder + dir + '/' + f
                    if os.path.getsize(image_file) > 0:
                        # Upload the image file, to get upload token
                        upload_token = upload(service, image_file)
                        if upload_token:
                            d = {
                                "albumId": album_id,
                                "newMediaItems": [
                                    {
                                        "simpleMediaItem": {
                                            "uploadToken": upload_token.decode('utf-8')
                                        }
                                    }
                                ]
                            }
                            # Add the image (upload token), to the album
                            ret = service.mediaItems().batchCreate(body=d).execute(http=http)
                            moveto_archive(image_file, dir)

                    print("Photos", image_file)


if __name__ == '__main__':
    main()