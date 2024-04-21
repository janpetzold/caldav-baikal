# Need to setup with
#
# pip3 install docker azure-storage-file-share
#

import os
from azure.storage.fileshare import ShareFileClient
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Docker setup
CONTAINER_NAME = 'baikal'
FILE_PATH_IN_CONTAINER = '/var/www/baikal/Specific/db/db.sqlite'

# Azure setup
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
SHARE_NAME = 'baikaldb'
FILE_DIRECTORY = 'db'
FILE_NAME = 'db.sqlite'

def fetch_file_from_container():
    # Using Podman to copy the file from the container to host
    local_path = '/tmp/temp_db.sqlite'
    podman_command = f"podman cp {CONTAINER_NAME}:{FILE_PATH_IN_CONTAINER} {local_path}"
    result = subprocess.run(podman_command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("Error fetching file from container:", result.stderr)
    else:
        print("File fetched from container.")

def upload_to_azure():
    file_client = ShareFileClient.from_connection_string(conn_str=CONNECTION_STRING, share_name=SHARE_NAME, file_path=os.path.join(FILE_DIRECTORY, FILE_NAME))
    with open('/tmp/temp_db.sqlite', 'rb') as data:
        file_client.upload_file(data)
    print("File uploaded to Azure File Storage.")

def main():
    fetch_file_from_container()
    upload_to_azure()

if __name__ == "__main__":
    main()
