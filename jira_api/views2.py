from jira_poc import jira_client
from jira_poc import app
from jira_poc.utility.jira_auth import get_jira_serialize_project



@app.route('/issues')
def searchIssue():
    try:
        issues_in_proj = jira_client.search_issues("project='jira projrct'")
        print("issues_in_proj=======================>",issues_in_proj)
        project_data_list = [get_jira_serialize_project(project) for project in issues_in_proj]
        return {"text":" success","project_list":project_data_list}
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