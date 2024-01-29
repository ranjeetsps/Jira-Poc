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
            # Retrieve the Issue Types for the specified project (e.g., "RISK")
            createmeta = jira_client.createmeta(projectKeys="RISK")
            
            # Extract the list of issue types from the create metadata
            issue_types = createmeta.get('projects', [])[0].get('issuetypes', [])

            return jsonify({"text": "Success", "issue_type_list": issue_types})
        
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})




class ListIssueLinkTypes(MethodView):
    def get(self):
        """
        Summary: This class handles the endpoint for retrieving all the link types present on Jira.
        It can be used to provide data in a dropdown while linking the risk to another ticket.
        """
        try:
            # Retrieve all available issue link types using the jira_client
            all_link_types = jira_client.issue_link_types()
            
            # Serialize each link type using the get_jira_serialized_object function
            issue_link_types_list = [get_jira_serialized_object(link_type) for link_type in all_link_types]
            
            # Return a JSON response with success and the list of issue link types
            return jsonify({"text": "Success", "link_types": issue_link_types_list})
        
        except Exception as E:
            # Return a JSON response with failure and the error message
            return jsonify({"text": "Failed", "error": str(E)})


class ListFields(MethodView):
    def get(self):
        """
        Summary: Lists all the  fields.
        """
        try:
            # Retrieve the project details for the specified project (e.g., "RISK")
            project = jira_client.project("RISK")
            
            # Retrieve all available custom fields using the jira_client
            fields = jira_client.fields()
            
            return jsonify({"text": "Success", "fields": fields})
        
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})









class ListIssuesByProjectName(MethodView):
    def get(self, project_name):
        try:
            # Search for issues in the specified project using JQL (Jira Query Language)
            issues_in_proj = jira_client.search_issues(f"project={project_name}")
            
            # Serialize each issue using the get_jira_serialized_object function
            issue_list = [get_jira_serialized_object(issue) for issue in issues_in_proj]
            
            # Return a JSON response with success and the list of serialized issues
            return jsonify({"text": "Success", "issues": issue_list})
        
        except Exception as E:
            # Return a JSON response with failure and the error message
            return jsonify({"text": "Failed", "error": str(E)})

    



class SearchIssuesByName(MethodView):
    def get(self, summary_name):
        try:
            # Search for issues with summary containing the specified name using JQL (Jira Query Language)
            issues = jira_client.search_issues(f'summary~{summary_name}')
            
            # Serialize each issue using the get_jira_serialized_object function
            issues_list = [get_jira_serialized_object(issue) for issue in issues]
            
            return jsonify({"text": "Success", "issue_list": issues_list})
        
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})



class GetIssueByID(MethodView):
    def get(self,issueId):
        try:
            # Retrieve the details of the specified issue (e.g., "RISK-1")
            issue = jira_client.issue(issueId)
            
            # Extract relevant information from the issue
            status_name = issue.fields.status.name if issue.fields.status else None
            
            # Prepare a dictionary with key details of the issue
            data = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": status_name,
                "assignee": issue.fields.assignee,
                "impact" : issue.fields.customfield_10035.value ,
                "likelyhood" : issue.fields.customfield_10034.value,
            }
            return jsonify({"text": "Success", "issue": data})
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})



class CreateRisk(MethodView):
    def post(self):
        """
        Summary: This view creates a Risk (ticket) on Jira.
        Input Data -
        issue_dict = {
            'project': {'id': 123},
            'summary': 'New issue from jira-python',
            'description': 'Look into this one',
            'issuetype': {'name': 'Bug'},
        }
        """
        try:
            # Extract JSON data from the request
            req_data = request.json 

            # Create a new issue on Jira using the provided issue_dict
            new_issue = jira_client.create_issue(req_data['issue_dict'])
            
            # Update a custom field for the new issue (e.g., customfield_10035 with value "1 - Low", Impact and likelyhood)
            new_issue.update(fields={"customfield_10035": {"value": "1 - Low"}})
            new_issue.update(fields={"customfield_10034": {"value": "1 - Rare"}})
            
            # Serialize the created issue using the get_jira_serialized_object function
            new_issue = [get_jira_serialized_object(new_issue)]
            
            return jsonify({"text": "Success", "issue": new_issue})
        
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})


class UpdateRisk(MethodView):
    def put(self):
        """
        Summary : This view updates a Risk (ticket) on jira .
        # new_issue.update(fields={'summary': 'new summary', 'description': 'A new summary was added'})
        """
        try:
            data = request.json
            issue = jira_client.issue(data["issue_id"])
            
            issue.update(summary=data["summary"], description = data["description"])
            issue.update(fields={"customfield_10035": {"value": data["impact"]}})
            issue.update(fields={"customfield_10034": {"value": data["likelyhood"]}})

            status_name = issue.fields.status.name if issue.fields.status else None
            new_data = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": status_name,
                "assignee": issue.fields.assignee ,
                "impact" : issue.fields.customfield_10035.value ,
                "likelyhood" : issue.fields.customfield_10034.value,
            }

            return jsonify({"text": " success", "status": 200, "message": "issues updated successfully", "updated data": new_data})
        except Exception as E:
            return jsonify({"text": " Failed", "error": str(E)})


class CreateIssueLink(MethodView):
    def post(self):
        """
        Summary : This view links an issue with another issue.
        risk_id  - Risk - Id of ticket
        link_id - linked issue -  id of the ticket
        outwardIssue - linked issue -  id of the ticket
        linkType -  get from the ListIssueLinkTypes
        """
        try:
            # Extract JSON data from the request
            data = request.json
            # Create a link between two issues using the specified data
            jira_client.create_issue_link(inwardIssue=data["risk_id"], outwardIssue=data["link_id"], type=data["linkType"])
            return jsonify({"text": "Success", "status": 200, "message": "Issues linked successfully"})
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})


class CreateIssueLink(MethodView):
    def post(self):
        """
        Summary : This view links an issue with another issue.
        risk_id  - Risk - Id of ticket
        link_id - linked issue -  id of the ticket
        outwardIssue - linked issue -  id of the ticket
        linkType -  get from the ListIssueLinkTypes
        """
        try:
            # Extract JSON data from the request
            data = request.json
            # Create a link between two issues using the specified data
            jira_client.create_issue_link(inwardIssue=data["risk_id"], outwardIssue=data["link_id"], type=data["linkType"])
            return jsonify({"text": "Success", "status": 200, "message": "Issues linked successfully"})
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})

class IssueLink(MethodView):
    def get(self,id):
        """
        id =  issue id
        gets all the links of a risk
        """
        try:
            import json
            issue = jira_client.issue(f'{id}')
            linked_issues =issue.fields.issuelinks

            linked_issues = [get_jira_serialized_object(link) for link in linked_issues]
            return jsonify({"message": "Success", "linked_issues":linked_issues,"count":len(linked_issues)})
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})

    def delete(self,id):
        """
        id =  link id
        gets all the links of a risk
        """
        try:
            jira_client.delete_issue_link(id)        
            return jsonify({"message": "Removed Link From Risk"})
        except Exception as E:
            return jsonify({"text": "Failed", "error": str(E)})



# jira.assign_issue(issue, 'newassignee')


jiraBlueprint.add_url_rule('/projects', view_func=ListProjects.as_view('projects'))
jiraBlueprint.add_url_rule('/issue_types', view_func=ListIssueTypes.as_view('issue_types'))

jiraBlueprint.add_url_rule('/issue_link_types', view_func=ListIssueLinkTypes.as_view('issue_link_types'))
jiraBlueprint.add_url_rule('/create_risk', view_func=CreateRisk.as_view('create_risk'))
jiraBlueprint.add_url_rule('/update_risk', view_func=UpdateRisk.as_view('update_risk'))


jiraBlueprint.add_url_rule("/link_issue", view_func=CreateIssueLink.as_view("create_issue_link"))
jiraBlueprint.add_url_rule("/linked_issue/<string:id>", view_func=IssueLink.as_view("linked_issue"))



jiraBlueprint.add_url_rule('/search_issues/<string:project_name>', view_func=ListIssuesByProjectName.as_view('list_issues_by_project_name'))
jiraBlueprint.add_url_rule('/search_issues_by_name/<string:summary_name>', view_func=SearchIssuesByName.as_view('search_issues_by_name'))
jiraBlueprint.add_url_rule('/get_issues_by_id/<string:issueId>', view_func=GetIssueByID.as_view('get_issues_by_id'))

jiraBlueprint.add_url_rule('/custom_fields', view_func=ListFields.as_view('custom_fields'))

