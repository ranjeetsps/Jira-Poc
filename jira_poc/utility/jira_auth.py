import requests, base64, codecs
import os
from jira import JIRA


def get_jira_auth_headers():

    print("JIRA_USERNAME=======>",os.getenv('JIRA_USERNAME'))

    username =  os.getenv('JIRA_USERNAME')
    api_token =  os.getenv('JIRA_SECRET_KEY')
    auth_string = f"{username}:{api_token}"
    encoded_auth_string = base64.b64encode(codecs.encode(auth_string, 'utf-8')).decode('utf-8')

    # Creating the Authorization header
    auth_header = {"Authorization": f"Basic {encoded_auth_string}"}
    return auth_header

def get_jira():
    """
    Retrieves or initializes the global JIRA client instance.

    Returns:
        JIRA: A JIRA client instance connected to the specified JIRA server.
    """

    # Creating the JIRA client instance with the specified options and authentication details
    JIRA_GLOBAL = JIRA(
        {"server":os.getenv('JIRA_SERVER')},
        basic_auth=(
            os.getenv('JIRA_USERNAME'),
            os.getenv('JIRA_SECRET_KEY')
        )
    )

    # Return the initialized JIRA client
    return JIRA_GLOBAL


def get_jira_serialized_object(data):
    serialized_project = {}
    for key, value in data.__dict__.items():
        # Convert non-serializable values to strings
        serialized_value = str(value) if isinstance(value, (type(None), str, int, float, bool)) else repr(value)
        serialized_project[key] = serialized_value
    return serialized_project
