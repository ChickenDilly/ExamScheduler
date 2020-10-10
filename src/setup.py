import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']
# insert path to credentials file
CREDENTIALS_FILE = os.path.join(os.path.abspath('credentials'), 'credentials.json')


def setup():
    creds = None
    # Passes service access the user's calendar to other functions.

    # The file token.pickle stores the user's access and refresh tokens in the
    # credentials folder, and is created automatically when the authorization
    # flow completes for the first time.

    try:
        os.chdir('credentials')
    except FileNotFoundError:
        os.mkdir('credentials')
        os.chdir('credentials')

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    os.chdir('../')

    return build('calendar', 'v3', credentials=creds)



