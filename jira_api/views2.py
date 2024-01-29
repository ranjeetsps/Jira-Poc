
from flask import request, jsonify, Blueprint
from flask.views import MethodView
import requests, base64, codecs
from jira_api.views import jiraBlueprint

import os

from jira_poc.utility.jira_auth import get_jira_serialized_object
# Jira
from jira_poc import jira_client



class AddComment(MethodView):
    def post(self):
        '''
        Summary: This api is used to add comment under an issue by issue id ,body and visibility(optional)
        '''
        try:
            data = request.json
            # Add a comment on an issues 
            jira_client.add_comment(issue = data["issue_id"],body =data["comment_body"])
            
            return jsonify({"text": "Success","status":201, "message": "Your comment added successfully"})
        
        except Exception as E:
            return jsonify({"text": "Failed", "status":500 ,"error": str(E)})


class GetCustomFieldData(MethodView):
    def get(self):
        '''
        Summary: This api is used to get options of custom field
        '''
        id = "customfield_10034"
        try:
            # get data of custom field 
            # custom_field = jira_client.fields()
            # print("custom_field====================>",custom_field)
        

         #Replace these with your Jira server URL, username, and password/token
            JIRA_SERVER = 'https://ranjeet-upwork-softprodigy.atlassian.net/'
            USERNAME = 'ritesh_poddar@softprodigy.com'
            PASSWORD = 'ATATT3xFfGF0FEq0HX3iAO5ng3DbDykntn8FOGJA9gGWXWSZ8uv0qWY0UiIbZurss4v15naK1FSlOg5BmHDme_Fux4SlcdcDIsYT9wL8m2umaUA5lSu_fSBeRfwaEDGNEo2tBJJWvufj1XRAdTWSU5GO94RM4-TsgV7NP_pDVbPp3uzKJ-3iklM=438D821F'
            # Replace 'CUSTOM_FIELD_ID' with the ID of your custom field
            custom_field_id = id
            # Jira REST API endpoint for custom field options
            api_url = f'{JIRA_SERVER}/rest/api/2/customField/{custom_field_id}/option'
            # Authentication credentials
            auth_credentials = (USERNAME, PASSWORD)
            # Make a GET request to retrieve options
            response = requests.get(api_url, auth=auth_credentials)
            # Check if the request was successful (status code 200)
            print("response==============================>",response)
            if response.status_code == 200:
                options = response.json()
                print("options===================>",options)
                for option in options:
                    print("vaue_of_options===============================>",option.get('value'))
            else:
                print(f"Failed to retrieve options. Status code: {response.status_code}")
                print(response.text)

            return jsonify({"text": "Success","status":201, "message": "custom_field"})
        except Exception as E:
            return jsonify({"text": "Failed", "status":500 ,"error": str(E)})




jiraBlueprint.add_url_rule('/add_comment', view_func=AddComment.as_view('add_comment'))
jiraBlueprint.add_url_rule('/get_custom_field', view_func=GetCustomFieldData.as_view('get_custom_field'))