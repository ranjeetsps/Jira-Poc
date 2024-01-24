from jira_poc import jira_client
from jira_poc import app
from jira_poc.utility.jira_auth import get_jira_serialize_project
from flask import request,jsonify



@app.route('/issues/<string:name>')
def searchIssue(name):
    try:
        issues_in_proj = jira_client.search_issues(f"project={name}")
        print("issues_in_proj=======================>",issues_in_proj)
        project_data_list = [get_jira_serialize_project(project) for project in issues_in_proj]
        return {"text":" success","project_list":project_data_list}
    except Exception as E:
            return {"text":" Failed","error":str(E)}


@app.route('/issues_by_name/<string:name>')
def searchIssueByName(name):
    try:
        issues_in_proj = jira_client.search_issues(f'summary~{name}')
        print("issues_in_proj=======================>",issues_in_proj)
        project_data_list = [get_jira_serialize_project(project) for project in issues_in_proj]
        return {"text":" success","project_list":project_data_list}
    except Exception as E:
            return {"text":" Failed","error":str(E)}
    

@app.route('/issues_by_id')
def searchIssueByID():
    try:
          
        issue = jira_client.issue("RISK-1")
        status_name = issue.fields.status.name if issue.fields.status else None

        data = {
               "key": issue.key,
                "summary" :issue.fields.summary,
                "description" :issue.fields.description,
                "status" :status_name,
                "assignee" :issue.fields.assignee
                        }
        return jsonify({"text":" success","issue":data})
    except Exception as E:
            return {"text":" Failed","error":str(E)}



########################### IMPORTANT #########################

# @app.route('/issue_types')
# def searchIssueTypes():
#     try:
#         # issues_in_proj = jira_client.project_issue_types("project='jira projrct'", startAt=0, maxResults=50)
#         issues_in_proj = jira_client.issue_types()
#         print("issues_in_proj=======================>",issues_in_proj)
#         project_data_list = [get_jira_serialize_project(project) for project in issues_in_proj]
#         return {"text":" success","project_list":project_data_list}
#     except Exception as E:
#             return {"text":" Failed","error":str(E)}
    

@app.route('/issue_link_types')
def searchIssueLinkTypes():
    try:
        # issues_in_proj = jira_client.project_issue_types("project='jira projrct'", startAt=0, maxResults=50)
        issues_in_proj = jira_client.issue_link_types()
        print("issues_in_proj=======================>",issues_in_proj)
        project_data_list = [get_jira_serialize_project(project) for project in issues_in_proj]
        return {"text":" success","project_list":project_data_list}
    except Exception as E:
            return {"text":" Failed","error":str(E)}


@app.route("/issue_type_by_project")
def get(self):
    # Get the list of the prujects
    try:
        createmeta = jira_client.createmeta(projectKeys="RISKEVENT")
        # Extracting issue type names
        issue_types = createmeta.get('projects', [])[0].get('issuetypes', [])
        return {"text":" success","issue_type_list":issue_types}
    except Exception as E:
        return {"text":" Failed","error":str(E)}
    


############################# CREATE LINK ISSUE ####################################



@app.route("/create/issue_link",methods =["POST"])
def createIssueLink():
    # Get the list of the prujects
    try:
        data = request.json
        link_data = {
        'inwardIssue': {'key': data["inwardIssue"]},
        'outwardIssue': {'key': data["outwardIssue"]},
        'type': {'name': data["linkType"]}  # Replace with the link type you want to use
    }
        # jira_client.create_issue_link(link_data)
        jira_client.create_issue_link(inwardIssue = data["inwardIssue"],outwardIssue = data["outwardIssue"],type = data["linkType"])

        return {"text":" success","status":200,"message":"issues linked successfully"}
    except Exception as E:
        return {"text":" Failed","error":str(E)}


@app.route("/update/issue",methods =["POST"])
def updateIssue():
    # Get the list of the prujects
    try:
        data = request.json
        issue = jira_client.issue(data["issue_id"])
        for field_name in issue.raw['fields']:
            print("field_name======================",field_name)
        issue.update(summary=data["summary"], description=data["description"])
        status_name = issue.fields.status.name if issue.fields.status else None
        new_data = {
               "key": issue.key,
                "summary" :issue.fields.summary,
                "description" :issue.fields.description,
                "status" :status_name,
                "assignee" :issue.fields.assignee
                        }

        return {"text":" success","status":200,"message":"issues updated successfully","updated data":new_data}
    except Exception as E:
        return {"text":" Failed","error":str(E)}