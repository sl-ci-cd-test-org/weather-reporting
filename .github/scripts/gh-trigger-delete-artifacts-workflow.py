# Import libraries
import sys
import requests
import json
from requests.auth import HTTPBasicAuth
from helpers import *
import os

#Arguments send by position:
    # 0.script_name
    # 1.gh_ref
    # 2.gh_token

if __name__ == '__main__':
    
    # Capture arguments
    gh_ref = sys.argv[1]
    gh_token = sys.argv[2]
    
    # Print arguments
    print(f"""-- Command line arguments --
        gh_ref: {gh_ref}
        gh_token: {gh_token}""")

    # Trigger delete-artifacts-workflow
    gh_run_workflow(gh_ref, gh_token, "delete-artifacts.yaml")