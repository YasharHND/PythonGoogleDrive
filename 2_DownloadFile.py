import io
import os

from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload

import ServiceAccountClient

load_dotenv()

USER_EMAIL = os.getenv('DELEGATED_USER_EMAIL')
SERVICE_ACCOUNT_FILE = 'resources/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
UPLOADED_FILE_ID = os.getenv('UPLOADED_FILE_ID')

service = ServiceAccountClient.build_delegated(SERVICE_ACCOUNT_FILE, USER_EMAIL, SCOPES)
request = service.files().get_media(fileId=UPLOADED_FILE_ID)
fh = io.FileIO('resources/downloaded_file.jpeg', 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while not done:
    status, done = downloader.next_chunk()
    print(f"Download {int(status.progress() * 100)}%")
