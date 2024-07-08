import os
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from googleapiclient.http import MediaIoBaseUpload

import ServiceAccountClient

load_dotenv()

USER_EMAIL = os.getenv('DELEGATED_USER_EMAIL')
SERVICE_ACCOUNT_FILE = 'resources/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
BINARY_UPLOAD_FOLDER_ID = os.getenv('BINARY_UPLOAD_FOLDER_ID')

service = ServiceAccountClient.build_delegated(SERVICE_ACCOUNT_FILE, USER_EMAIL, SCOPES)
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_to_drive():
    file_name = request.headers.get('X-File-Name')
    file_data = request.get_data()

    if not file_name:
        return jsonify({'error': 'Missing file_name'}), 400

    if not file_data:
        return jsonify({'error': 'Empty file_data'}), 400

    print(f'Received file data of length: {len(file_data)}')
    file_metadata = {
        'name': file_name,
        'parents': [BINARY_UPLOAD_FOLDER_ID]
    }
    file = service.files().create(
        body=file_metadata,
        media_body=MediaIoBaseUpload(BytesIO(file_data), mimetype='application/octet-stream')
    ).execute()
    return jsonify({'file_id': file.get('id')}), 200


if __name__ == '__main__':
    app.run(debug=True)
