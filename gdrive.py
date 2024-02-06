import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def main():
  lista= {}
  listb= {} 
  files = []
  page_token = None
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  try:
    service = build("drive", "v3", credentials=creds)
    response = service.files().list(
      q = "mimeType = 'application/vnd.google-apps.folder'",
          spaces="drive",
          fields="nextPageToken, files(id, name)",
          pageToken=page_token
    ).execute()

    for file in response.get("files", []):
      lista[file.get("name")] = file.get("id")
    files.extend(response.get("files", []))
    page_token = response.get("nextPageToken", None)
    
    for i in enumerate(lista,1):
      print(str(i[0]) + ": " + i[1]) 
    
    while True:
      try:
        num = int(input("please choose the folder Number: "))
        folderNames = dict(enumerate(lista.keys(),1))
        folderName = folderNames.get(num)
        folderId = lista.get(folderName)
        if folderId == None:
          continue
        break

      except Exception as e:
        print(e)
        exit()

    response = service.files().list(
      q =  "'" + folderId + "' in parents",
          fields="nextPageToken, files(id, name, mimeType)",
          pageToken=page_token
    ).execute()

    for file in response.get("files", []):
      listb[file.get("id")] = file.get("name")
     

    files.extend(response.get("files", []))
    page_token = response.get("nextPageToken", None)
    
    if len(listb) == 0:
      exit("No files are present in that folder")

    for i in enumerate(listb.values(),1):
      print(str(i[0]) + ": " + i[1])
    
    while True:
      try:
        num = int(input("please choose the file Number you want to download: "))
      
        fileNames = dict(enumerate(listb.keys(),1))
    
        Id = fileNames.get(num)
        fileName = listb[Id]
       
        break
      except Exception as e:
        print(e)
       
    services = build("drive", "v3", credentials=creds)
    request = services.files().get_media(fileId=Id)    
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download Progress: {int(status.progress() * 100)}.")
    try:
      with open(fileName,'xb') as f:
        f.write(file.getvalue())
        
    except FileExistsError:
      with open(fileName,'wb') as f:
        f.write(file.getvalue())
  
  
  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None
  return files

if __name__ == "__main__":
  main()