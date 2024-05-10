# Import libraries
import sys
import requests
import json
from requests.auth import HTTPBasicAuth
from helpers import *
import os

if __name__ == '__main__':
    # Capture arguments
    gh_ref = sys.argv[1]
    gh_token = sys.argv[2]
    # Print arguments
    print(f"-- Command line arguments --\n\tgh_ref: {gh_ref}\n\tgh_token: {gh_token} ")

    artifacts = gh_list_artifacts(gh_ref, gh_token)["artifacts"]
    # print(artifacts)

    for artifact in artifacts:
        # print(artifact["id"])
        gh_delete_artifact(gh_ref, gh_token, artifact["id"])
        # break