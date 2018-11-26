import os
import shutil
import httplib2
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import requests
import _thread
from threading import Thread
import subprocess


# https://stackoverflow.com/questions/51746830/can-upload-photo-when-using-the-google-photos-api/52021690#52021690

folder = '/Users/tanmoy.sil/Downloads/Test/'
archive_path = '/Users/tanmoy.sil/Downloads/Archive/'
error_path = '/Users/tanmoy.sil/Downloads/Error/'

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
    # print('\nUpload token: %s' % r.content)



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


def createItem(service, upload_token, albumId):
    d = {
        "albumId": album_id,
        "newMediaItems": [
            {
                "simpleMediaItem": {
                    "uploadToken": upload_token
                }
            }
        ]
    }
    ret = service.mediaItems().batchCreate(body=d).execute(http=http)
    print(ret)




    # url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
    #
    # body = {
    #     'newMediaItems': [
    #         {
    #             "description": "test upload",
    #             "simpleMediaItem": {
    #                 "uploadToken": upload_token
    #             }
    #         }
    #     ]
    # }
    #
    # if albumId is not None:
    #     body['albumId'] = albumId;
    #
    # bodySerialized = json.dumps(body);
    # headers = {
    #     'Authorization': "Bearer " + service._http.request.credentials.access_token,
    #     'Content-Type': 'application/json',
    # }
    #
    # r = requests.post(url, data=bodySerialized, headers=headers)
    # print ('\nCreate item response: %s' % r.content)
    # return r.content


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

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

http = httplib2.Http()
http = creds.authorize(http)
service = build('photoslibrary', 'v1', http=creds.authorize(Http()))
map_albums = get_all_albums(service, http)

for root, dirs, files in os.walk(folder):
    for dir in dirs:
        album_name = dir.strip()
        album_id = ''
        print ("Album ", album_name)
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
            album_id = album['id']


        #
        for root1, dir1, files1 in os.walk(folder+dir):
            threads = []
            for f in files1:
                image_file = folder + dir + '/' + f
                if os.path.getsize(image_file) > 0:
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
                        ret = service.mediaItems().batchCreate(body=d).execute(http=http)
                        if 'error' in ret:
                            if ret['code'] == 500:
                                http = httplib2.Http()
                                http = creds.authorize(http)
                                service = build('photoslibrary', 'v1', http=creds.authorize(Http()))

                moveto_archive(image_file, dir)

                print("Photos", image_file)

