from flask import request, jsonify, Blueprint
from flask.views import MethodView
import requests, base64, codecs
jiraBlueprint = Blueprint('apiBlueprint', "__name__")
import os

from jira_poc.utility.jira_auth import get_jira_serialize_project
# Jira
from jira_poc import jira_client




@jiraBlueprint.route("/testapi")
def GetProjects():
    return jsonify({"status":200,"message":"Jira APi hit"})



class Projects(MethodView):


    def get(self):
        try:
            projects = jira_client.projects()
            print(projects)
            project_data_list = [get_jira_serialize_project(project) for project in projects]

            return jsonify({"text":" success","project_list":project_data_list})
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})


jiraBlueprint.add_url_rule('/projects', view_func=Projects.as_view('projects'))
