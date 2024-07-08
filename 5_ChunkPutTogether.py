import io
import os

from dotenv import load_dotenv
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

import ServiceAccountClient

load_dotenv()

USER_EMAIL = os.getenv('DELEGATED_USER_EMAIL')
SERVICE_ACCOUNT_FILE = 'resources/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
BINARY_UPLOAD_FOLDER_ID = os.getenv('BINARY_UPLOAD_FOLDER_ID')
IMAGE_UPLOAD_FOLDER_ID = os.getenv('IMAGE_UPLOAD_FOLDER_ID')

service = ServiceAccountClient.build_delegated(SERVICE_ACCOUNT_FILE, USER_EMAIL, SCOPES)


def list_files_in_folder(folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        orderBy='name',
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])


def download_chunks_and_combine(binary_folder_id, image_folder_id, output_filename):
    chunks = list_files_in_folder(binary_folder_id)
    complete_image_stream = io.BytesIO()
    for chunk in chunks:
        request = service.files().get_media(fileId=chunk['id'])
        downloader = MediaIoBaseDownload(complete_image_stream, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
    complete_image_stream.seek(0)
    file_metadata = {
        'name': output_filename,
        'parents': [image_folder_id]
    }
    media = MediaIoBaseUpload(complete_image_stream, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')


file_id = download_chunks_and_combine(BINARY_UPLOAD_FOLDER_ID, IMAGE_UPLOAD_FOLDER_ID, 'complete.jpg')
print('File ID:', file_id)
