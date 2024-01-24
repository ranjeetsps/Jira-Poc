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
    """
    Summary: This class handles the endpoint for retrieving Jira projects and serializes the project data.
    """
    def get(self):
        try:
            # Retrieve the list of projects using the jira_client
            projects = jira_client.projects()
            # Serialize each project using the get_jira_serialize_project function
            project_data_list = [get_jira_serialize_project(project) for project in projects]
            return jsonify({"text": "Success", "project_list": project_data_list})
        except Exception as E:
            # Return a JSON response with failure and the error message
            return jsonify({"text": "Failed", "error": str(E)})

class IssueTypes(MethodView):
    def get(self):
        """
        Summary: This class handles the endpoint for retrieving all the issue types in a Project.
        """
        try:
            createmeta = jira_client.createmeta(projectKeys="RISKEVENT")
            issue_types = createmeta.get('projects', [])[0].get('issuetypes', [])
            return jsonify({"text":" success","issue_type_list":issue_types})
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})


class IssueLinkTypes(MethodView):
    def get(self):
        """
        Summary: This class handles the endpoint for retrieving all the link types present on jira.
        it can be used to give the data in dropdown while linking the risk to another ticket.
        """
        try:
            all_link_types = jira_client.issue_link_types()
            issue_link_types_list = [get_jira_serialize_project(link_type) for link_type in all_link_types]
            return jsonify({"text":" success","link_types":issue_link_types_list})
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})

class CreateRisk(MethodView):
    def post(self):
        """
        Summary : This view creates a Risk (ticket) on jira .
        Input Data - 
        issue_dict = {
            'project': {'id': 123}, 
            'summary': 'New issue from jira-python',
            'description': 'Look into this one',
            'issuetype': {'name': 'Bug'},
        }
        """
        return jsonify({"text":" success"})
        
        # new_issue = jira.create_issue(project='PROJ_key_or_id', summary='New issue from jira-python',
        #                       description='Look into this one', issuetype={'name': 'Bug'})
    







# jira.assign_issue(issue, 'newassignee')






jiraBlueprint.add_url_rule('/projects', view_func=Projects.as_view('projects'))
jiraBlueprint.add_url_rule('/issues', view_func=IssueTypes.as_view('issues'))
jiraBlueprint.add_url_rule('/issue_link_types', view_func=IssueLinkTypes.as_view('issue_link_types'))
