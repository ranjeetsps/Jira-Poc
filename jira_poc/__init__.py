from flask import Flask 

# Blueprints
app = Flask(__name__)

# Implement environment
import  os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()




from jira_api.views import jiraBlueprint
app.register_blueprint(jiraBlueprint, url_prefix ='/jira')
