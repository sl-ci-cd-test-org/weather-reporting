# Import libraries
import sys
import json
from requests.auth import HTTPBasicAuth
from helpers import *

# Arguments send by position:
    # 0.script_name
    # 1.sl_email
    # 2.sl_pw
    # 3.sl_source_org
    # 4.sl_target_org
    # 5.sl_source_pspace
    # 6.sl_target_pspace
    # 7.sl_source_project
    # 8.sl_target_project

if __name__ == '__main__':

    # Capture arguments
    sl_email = sys.argv[1]
    sl_pw = sys.argv[2]
    sl_source_org = sys.argv[3]
    sl_target_org = sys.argv[4]
    sl_source_pspace = sys.argv[5]
    sl_target_pspace = sys.argv[6]
    sl_source_project = sys.argv[7]
    sl_target_project = sys.argv[8]
    sl_auth = HTTPBasicAuth(sl_email, sl_pw)

    # Print arguments
    print(f"""-- Command line arguments --
        sl_email: {sl_email}
        sl_pw: {sl_pw}
        sl_source_org: {sl_source_org}
        sl_target_org: {sl_target_org}
        sl_source_pspace: {sl_source_pspace}
        sl_target_pspace: {sl_target_pspace}
        sl_source_project: {sl_source_project}
        sl_target_project: {sl_target_project}""")

    # Retrieve all tasks from the source project
    source_tasks = sl_list_assets(sl_source_org, sl_source_pspace, sl_source_project, sl_auth, "Job")
    
    # Filter source tracked tasks
    source_tasks = sl_filter_tracked_assets(source_tasks)
    
    # Filter source triggered tasks
    source_tasks = list(filter(lambda x: x["metadata"]["type"] == "triggered" , source_tasks))

    # Map source tasks properties
    source_tasks = list(map(lambda x: {"name":x["name"], "snode_id": x["snode_id"], "task_type": x["metadata"]["type"]},source_tasks))

    # Check if project exists in target organization
    if sl_check_project_existence(sl_target_org, sl_target_pspace, sl_target_project, sl_auth):
        # Retrieve target tasks
        target_tasks = sl_list_assets(sl_target_org, sl_target_pspace, sl_target_project, sl_auth, "Job")
        # Filter target tracked tasks
        target_tasks = sl_filter_tracked_assets(target_tasks)        
        # Filter target triggered tasks
        target_tasks = list(filter(lambda x: x["metadata"]["type"] == "triggered" , target_tasks))
        # Map target tasks properties
        target_tasks = list(map(lambda x: {"name":x["name"], "snode_id": x["snode_id"], "task_type": x["metadata"]["type"]},target_tasks))
    else:
        # Target project does not exist
        target_tasks = []

    # Tasks list initialization
    tasks = []

    # Check if source task exists in target_tasks
    for source_task in source_tasks:
        found = False
        for target_task in target_tasks:
            if source_task["name"] == target_task["name"]:
                found = True
                tasks.append(target_task)
                break
        if found == False:
            tasks.append(source_task)
   
    # Task config initialization
    tasks_config = []

    # Get and map task details
    for task in tasks:
        task_details = sl_get_task_details(sl_auth, snode_id=task["snode_id"])
        task_details = {
            "job_name":task_details["job_name"],
            "token":task_details["parameters"]["llfeed_token"]
        }
        tasks_config.append(task_details)

    # Set tasks config dictionary
    tasks_config = {
        "tasks":tasks_config
    }

    # Save tasks config file
    with open("tasks-config.json", "w") as json_file:
        json.dump(tasks_config, json_file)

    print(f"\t- Task config successfully generated! -")