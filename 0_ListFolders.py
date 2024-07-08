import os

from dotenv import load_dotenv

import ServiceAccountClient

load_dotenv()

USER_EMAIL = os.getenv('DELEGATED_USER_EMAIL')
SERVICE_ACCOUNT_FILE = 'resources/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = ServiceAccountClient.build_delegated(SERVICE_ACCOUNT_FILE, USER_EMAIL, SCOPES)
results = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                               fields='nextPageToken, files(id, name)').execute()
folders = results.get('files', [])
if not folders:
    print('No folders found.')
else:
    print('Folders:')
    for folder in folders:
        print(f"{folder['name']} ({folder['id']})")
