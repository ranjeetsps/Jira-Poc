from jira_poc import jira_client
from jira_poc import app
from jira_poc.utility.jira_auth import get_jira_serialized_object
from flask import request,jsonify



@app.route('/issues/<string:project_name>')
def ListIssuesByProjectName(project_name):
    try:
        issues_in_proj = jira_client.search_issues(f"project={project_name}")
        print("issues_in_proj=======================>",issues_in_proj)
        project_data_list = [get_jira_serialized_object(project) for project in issues_in_proj]
        return {"text":" success","project_list":project_data_list}
    except Exception as E:
            return {"text":" Failed","error":str(E)}


@app.route('/issues_by_name/<string:summary_name>')
def SearchIssuesByName(summary_name):
    try:
        issues_in_proj = jira_client.search_issues(f'summary~{summary_name}')
        print("issues_in_proj=======================>",issues_in_proj)
        project_data_list = [get_jira_serialized_object(project) for project in issues_in_proj]
        return {"text":" success","project_list":project_data_list}
    except Exception as E:
            return {"text":" Failed","error":str(E)}
    

@app.route('/issues_by_id')
def SearchIssueByID():
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



@app.route("/create/issue_link",methods =["POST"])
def createIssueLink():
    # Get the list of the prujects
    try:
        data = request.json
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