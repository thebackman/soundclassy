""" exports all sqlite data to google drive for import into google colab """


# -- libs


from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import os
import datetime
import sqlite3
import confs
import pandas as pd


# -- paths and globals


cred_dir = os.path.join(os.getcwd(), "cfg")
cred_token = os.path.join(cred_dir, "token.json")
cred_cred = os.path.join(cred_dir, "credentials.json")
SCOPES = ['https://www.googleapis.com/auth/drive']
target_file = "decibel.csv"


# -- functions


def get_csv():
    q = "select * from decibel;"
    conn = sqlite3.connect(confs.db_path)
    df = pd.read_sql_query(q, con = conn)
    df.to_csv("decibel.csv")
    conn.close()


def delete_csv():
    os.remove("decibel.csv")
    

def authenticate_and_send():
    """ from https://developers.google.com/drive/api/v3/quickstart/python """

    creds = None

    if os.path.exists(cred_token):
        creds = Credentials.from_authorized_user_file(cred_token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_cred, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cred_token, 'w') as token:
            token.write(creds.to_json())

    # get the client
    service = build('drive', 'v3', credentials=creds)
    
    # upload the csv file into the specified folder
    now = datetime.datetime.now()
    folder_id = '15SvIfazK6dmpoOjsDBcFRjb8kvAaL1kM'
    file_metadata = {'name': f'decibel_{now}.csv', 'parents': [folder_id]}
    media = MediaFileUpload(target_file, mimetype='text/csv')
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

if __name__ == '__main__':
    # get data
    get_csv()
    # send it
    authenticate_and_send()
    # delete extracted data
    delete_csv()
