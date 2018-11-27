# Flickr to Google Photos - Bulk Uploader
### Preface
In November 2018, Flicker announced limitation of 1000 photos free account. If any user had more then 1000 photos (previously flickr had free limit of 1TB), it will be deleted.
Many user looked for alternatives and Google photos seems very promicing, as it is providing unlimited photo storage (with 16 mega-pixel limit).
Flickr will allow user to download its metadata and photos. This photos can be uploaded to Google Photos later on using Google Photos _Backup and Sync_ app. But this app can't create Album and ofcourse don't understand Flickr metadata. There are some market available tools for this but they are expensive.
 
This project I build some python script which will read flickr downloaded (unzipped) files, put them in a directory structures and then upload them in Google Photos with Albums.


### How to execute
1. CreateFolderStructure.py - This will create Album based folder structure locally based on flickr downloaded pictures. 
2. GPhotoUploader.py - This will upload all the photos, albums from the folder structure created above steps.

_Optional Step:_ DataSanityCheck.Py is used to find file not part of any Albums and put them under Un-categorized
folder. 

### Notes
- You might want to take Google Storage Subscription during this upload process, because uploader will upload the file in full resolution. Once the files are uploaded you can resize it via Google Photos -> Settings -> `Recover Storage`. This will take some time to resize your photos 16 meg size which is unlimited. Once the process is complete you can unsubscribe from additional storage.
- `credentials.json` - we need this file for authentication purpose. Please read this link [Get started with REST](https://developers.google.com/photos/library/guides/get-started), to obtain an credential from Google. 
    
