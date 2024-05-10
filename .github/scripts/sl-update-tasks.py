# Import libraries
import sys
import json
from requests.auth import HTTPBasicAuth
from helpers import *
import os

#Arguments send by position:
    # 0.script_name
    # 1.sl_email
    # 2.sl_pw
    # 3.sl_org
    # 4.sl_target_pspace
    # 5.sl_target_project

if __name__ == '__main__':
    # Capture arguments
    sl_email = sys.argv[1]
    sl_pw = sys.argv[2]
    sl_target_org = sys.argv[3]
    sl_target_pspace = sys.argv[4]
    sl_target_project = sys.argv[5]
    sl_auth = HTTPBasicAuth(sl_email, sl_pw)

    # Print arguments
    print(f"""-- Command line arguments --
        sl_email: {sl_email}
        sl_pw: {sl_pw}
        sl_target_org: {sl_target_org}
        sl_target_pspace: {sl_target_pspace}
        sl_target_project: {sl_target_project}""")

    # Open tasks-config file
    print("-- Reading tasks-config.json file! --")
    try:
        with open("tasks-config.json","r") as file:
            tasks_config = json.load(file)["tasks"]
    except FileNotFoundError:
        exit("# The file does not exists! #")

    # List all tasks in the project
    tasks = sl_list_assets(sl_target_org, sl_target_pspace, sl_target_project, sl_auth, "Job")

    # Filter tracked tasks only
    tasks = sl_filter_tracked_assets(tasks)
    
    # Filter triggered tasks
    tasks = list(filter(lambda x: x["metadata"]["type"] == "triggered" , tasks))

    # Update triggered tasks
    for task in tasks:
        tasks_details = sl_get_task_details(sl_auth, snode_id=task["snode_id"])
        tasks_details["parameters"]["llfeed_token"] = list(filter((lambda x: x["job_name"] == tasks_details["job_name"]), tasks_config))[0]["token"]
        sl_update_triggered_task(sl_target_org, sl_target_pspace, sl_target_project, sl_auth, tasks_details)