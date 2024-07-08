import requests


def read_file_in_chunks(file_path, chunk_size=100 * 1024):
    chunk_idx = 1
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk_idx, chunk
            chunk_idx += 1


for idx, data in read_file_in_chunks('resources/source.jpg'):
    chunk_name = f'{idx:05d}'
    response = requests.post(
        'http://localhost:5000/upload',
        data=data,
        headers={
            'Content-Type': 'application/octet-stream',
            'X-File-Name': chunk_name
        }
    )
    if response.status_code != 200:
        print(f'Error uploading chunk {chunk_name}: {response.text}')
        break
    print(f'Uploaded chunk {chunk_name}')
print('File upload complete.')
