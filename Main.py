from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import httplib2
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

SCOPES = 'https://www.googleapis.com/auth/photoslibrary' #.readonly.appcreateddata'


# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    http = httplib2.Http()
    http = creds.authorize(http)
    # resp, content = http.request(
    #     uri='https://photoslibrary.googleapis.com/v1/albums',
    #     method='POST',
    #     headers={'Content-Type': 'application/json; charset=UTF-8'},
    #     body=json.dumps({'album': {'title': '123'}}),
    # )
    service = build('photoslibrary', 'v1', http=creds.authorize(Http()))
    request = service.albums().list()
    while request is not None:
        albums_in_photos = request.execute(http=http)
        if 'albums' in albums_in_photos:
            for album_in_photos in albums_in_photos['albums']:
                print(album_in_photos['title'])
        request = service.albums().list_next(request, albums_in_photos)
        print(request)

    # activities = service.albums()
    # request = activities.list()
    #
    # while request is not None:
    #     albums_in_photos = request.execute(http=http)
    #     print (albums_in_photos)
    #     # Do something with the activities
    #
    #     request = activities.list_next(request, albums_in_photos)

    # d = json.loads('{"album": { "title": "123"}}')
    # albums = service.albums().create(body=d).execute(http=http)
    # service.albums().create(title='Test123')
    # albums = service.albums().list().execute(http=http)
    # for album in albums['albums']:
    #     print(album['title'])
    # Create a new Album

    print(service.albums())
    # service = build('calendar', 'v3', http=creds.authorize(Http()))
    #
    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

if __name__ == '__main__':
    main()
#
#
# def main():
#     flow = client.flow_from_clientsecrets('credentials.json',
#                                    scope=SCOPES,
#                                    redirect_uri='http://example.com/auth_return')
#     auth_uri = flow.step1_get_authorize_url()
#     flow.
#     # http = httplib2.Http()
#
#     """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     store = file.Storage('credentials.json')
#     creds = store.get()
#     if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
#         creds = tools.run_flow(flow, store)
#     service = build('drive', 'v3', http=creds.authorize(Http()))
#
#     # Call the Drive v3 API
#     results = service.files().list(
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))
#
# if __name__ == '__main__':
#     main()