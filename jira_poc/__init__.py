from flask import Flask 
from jira_poc.utility.jira_auth import get_jira
# Blueprints
app = Flask(__name__)

# Implement environment
import  os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()

# Jjira client
jira_client = get_jira()


from jira_api.views import jiraBlueprint
from jira_api.views2 import *

app.register_blueprint(jiraBlueprint, url_prefix ='/jira')
