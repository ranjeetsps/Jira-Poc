from flask import request, jsonify, Blueprint
from flask.views import MethodView
import requests, base64, codecs
jiraBlueprint = Blueprint('apiBlueprint', "__name__")
import os

from jira_poc.utility.jira_auth import get_jira_auth_headers




@jiraBlueprint.route("/testapi")
def GetProjects():
    return jsonify({"status":200,"message":"Jira APi hit"})



class Projects(MethodView):
    def get(self):
        try:
            url = os.getenv('JIRA_HOST')+"project"
            response = requests.get(url, headers=get_jira_auth_headers())
            if response.status_code == 200:
                projects = response.json()
                print("projects=======",projects)
                for project in projects:
                    print(f"Project Key: {project['key']}, Project Name: {project['name']}")
            else:
                print(f"Error: {response.status_code}, {response.text}")
            return jsonify({"text":" Projects Get API hit","projects":projects})
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})



jiraBlueprint.add_url_rule('/projects', view_func=Projects.as_view('projects'))
