from google.oauth2 import service_account
from googleapiclient.discovery import build


def build_delegated(service_account_file, delegated_user_email, scopes):
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
    delegated_credentials = credentials.with_subject(delegated_user_email)
    return build('drive', 'v3', credentials=delegated_credentials)
