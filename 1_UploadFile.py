import os

from dotenv import load_dotenv
from googleapiclient.http import MediaFileUpload

import ServiceAccountClient

load_dotenv()

USER_EMAIL = os.getenv('DELEGATED_USER_EMAIL')
SERVICE_ACCOUNT_FILE = 'resources/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
FILE_PATH = 'resources/CMO.jpeg'
IMAGE_UPLOAD_FOLDER_ID = os.getenv('IMAGE_UPLOAD_FOLDER_ID')

service = ServiceAccountClient.build_delegated(SERVICE_ACCOUNT_FILE, USER_EMAIL, SCOPES)
file_metadata = {
    'name': 'CMO.jpeg',
    'parents': [IMAGE_UPLOAD_FOLDER_ID]
}
media = MediaFileUpload(FILE_PATH, resumable=True)
file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print('File ID: %s' % file.get('id'))
