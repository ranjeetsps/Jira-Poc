import requests, base64, codecs
from jira_poc import app
import os



def get_jira_auth_headers():

    print("JIRA_USERNAME=======>",os.getenv('JIRA_USERNAME'))

    username =  os.getenv('JIRA_USERNAME')
    api_token =  os.getenv('JIRA_SECRET_KEY')
    auth_string = f"{username}:{api_token}"
    encoded_auth_string = base64.b64encode(codecs.encode(auth_string, 'utf-8')).decode('utf-8')

    # Creating the Authorization header
    auth_header = {"Authorization": f"Basic {encoded_auth_string}"}
    return auth_header