from flask import request, jsonify, Blueprint
from flask.views import MethodView
import requests, base64, codecs


jiraBlueprint = Blueprint('apiBlueprint', "__name__")


import os

from jira_poc.utility.jira_auth import get_jira_serialized_object
# Jira
from jira_poc import jira_client


# customfield_10034 = Likelyhood
# customfield_10035 = IMpact




class ListProjects(MethodView):
    """
    Summary: This class handles the endpoint for retrieving Jira projects and serializes the project data.
    """
    def get(self):
        try:
            # Retrieve the list of projects using the jira_client
            projects = jira_client.projects()
            # Serialize each project using the get_jira_serialized_object function
            project_data_list = [get_jira_serialized_object(project) for project in projects]
            return jsonify({"text": "Success", "project_list": project_data_list})
        except Exception as E:
            # Return a JSON response with failure and the error message
            return jsonify({"text": "Failed", "error": str(E)})

class ListIssueTypes(MethodView):
    def get(self):
        """
        Summary: This class handles the endpoint for retrieving all the issue types in a Project.
        """
        try:
            createmeta = jira_client.createmeta(projectKeys="RISK")
            issue_types = createmeta.get('projects', [])[0].get('issuetypes', [])
            return jsonify({"text":" success","issue_type_list":issue_types})
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})


class ListIssueLinkTypes(MethodView):
    def get(self):
        """
        Summary: This class handles the endpoint for retrieving all the link types present on jira.
        it can be used to give the data in dropdown while linking the risk to another ticket.
        """
        try:
            all_link_types = jira_client.issue_link_types()
            issue_link_types_list = [get_jira_serialized_object(link_type) for link_type in all_link_types]
            return jsonify({"text":" success","link_types":issue_link_types_list})
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})


class ListCustomFields(MethodView):
    def get(self):
        """
        Summary: Lists all custom fields.
        """
        try:
            project = jira_client.project("RISK")

            fields = jira_client.fields()
            return jsonify({"text":" success","fields":fields})
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
        try:
            req_data = request.json 

            new_issue = jira_client.create_issue(req_data['issue_dict'])
            new_issue.update(fields={"customfield_10035": {"value" :"1 - Low"}})
            # 
            new_issue = [get_jira_serialized_object(new_issue) ]
            return jsonify({"text":" success","issue" :new_issue })
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})

class UpdateRisk(MethodView):
    def put(self):
        """
        Summary : This view updates a Risk (ticket) on jira .

                    # new_issue.update(fields={'summary': 'new summary', 'description': 'A new summary was added'})

        """
        try:
            issue = jira_client.issue("RISK-20")
            # print("issue.fields",issue.fields.__dict__)

            print(issue.fields.customfield_10034)
    



            # fields_dict = {}
            # for field_name, field_value in issue.fields.__dict__.items():
            #     if hasattr(field_value, '__dict__'):
            #         # If the field_value has its own __dict__, convert it to a plain dictionary
            #         fields_dict[field_name] = dict(field_value.__dict__)
            #     else:
            #         # If it doesn't have __dict__, just use the value as is
            #         fields_dict[field_name] = field_value

            # Print or use the fields_dict as needed
            # print("::::::::::::::::::::::")
            # print(fields_dict)

            return jsonify({"text":" success","issue" :"issue" })
        except Exception as E:
            return jsonify({"text":" Failed","error":str(E)})


# jira.assign_issue(issue, 'newassignee')

jiraBlueprint.add_url_rule('/custom_fields', view_func=ListCustomFields.as_view('custom_fields'))



jiraBlueprint.add_url_rule('/projects', view_func=ListProjects.as_view('projects'))
jiraBlueprint.add_url_rule('/issue_types', view_func=ListIssueTypes.as_view('issue_types'))
jiraBlueprint.add_url_rule('/issue_link_types', view_func=ListIssueLinkTypes.as_view('issue_link_types'))
jiraBlueprint.add_url_rule('/create_risk', view_func=CreateRisk.as_view('create_risk'))
jiraBlueprint.add_url_rule('/update_risk', view_func=UpdateRisk.as_view('update_risk'))


