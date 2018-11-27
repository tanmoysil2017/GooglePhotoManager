import httplib2
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/photoslibrary'

# Get all the Albums, WWS Paging implemented


def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    http = httplib2.Http()
    http = creds.authorize(http)
    service = build('photoslibrary', 'v1', http=creds.authorize(Http()))
    request = service.albums().list()
    while request is not None:
        albums_in_photos = request.execute(http=http)
        if 'albums' in albums_in_photos:
            for album_in_photos in albums_in_photos['albums']:
                print(album_in_photos['title'])
        request = service.albums().list_next(request, albums_in_photos)
        print(request)


if __name__ == '__main__':
    main()
