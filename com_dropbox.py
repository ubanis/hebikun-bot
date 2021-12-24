from dropbox import Dropbox
import os

DL_TOKEN = os.environ.get("DROPBOX_API_TOKEN")

def upload_file(file_path):
    """
    upload file to dropbox
    """
    dbx = Dropbox(DL_TOKEN)
    file_name = os.path.basename(file_path)
    dest_path = os.path.join('/', file_name)
    try:
        with open(file_path, 'rb') as local_file:
            dbx.files_upload(local_file.read(), dest_path, mute = True)
    except Exception as err:
        print(f"Failed to upload {file_name}\n{err}")
