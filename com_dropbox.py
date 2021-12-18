from dropbox import Dropbox
import os

DL_TOKEN = os.environ.get("DROPBOX_API_TOKEN")

def upload_file(file_path):
    dbx = Dropbox(DL_TOKEN)
    file_name = os.path.basename(file_path)
    dest_path = os.path.join('/', file_name)
    try:
        with open(file_path, 'rb') as f:
            dbx.files_upload(f.read(), dest_path, mute=True)
    except Exception as err:
        print('Failed to upload %s\n%s' % (file_name, err))
