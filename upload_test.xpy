from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    # Path to the credentials JSON file downloaded from the Google Cloud Console
    creds_path = 'path/to/credentials.json'

    # Load credentials from the file
    creds = None
    creds = Credentials.from_authorized_user_file(creds_path, SCOPES)

    return creds

def upload_file(service, file_path, folder_id=None):
    file_metadata = {
        'name': 'Your_File_Name',  # Replace with the desired file name
        'parents': [folder_id] if folder_id else None
    }

    media = MediaFileUpload(file_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f'File ID: {file["id"]}')

def main():
    # Authenticate using credentials
    credentials = authenticate()

    if credentials is None:
        return

    # Build the Google Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Replace 'path/to/upload/file.txt' with the actual path to the file you want to upload
    file_to_upload = 'path/to/upload/file.txt'

    # Replace 'YOUR_FOLDER_ID' with the ID of the folder where you want to upload the file (optional)
    folder_id = 'YOUR_FOLDER_ID'

    # Upload the file
    upload_file(drive_service, file_to_upload, folder_id)

if __name__ == '__main__':
    main()