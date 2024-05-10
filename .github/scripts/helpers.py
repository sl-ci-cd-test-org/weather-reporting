# Import libraries
import requests
import json
from urllib.parse import quote

def sl_check_project_existence(sl_org, sl_pspace, sl_project, sl_auth):
    # This function checks if the given project exists in SnapLogic.
    print(f"-- Checking the existence of project: {sl_org}/{sl_pspace}/{sl_project} --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/asset/list/{sl_org}/{sl_pspace}"
    payload = {}
    response = requests.request("GET", url, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] == 200:
        projects = list(map(lambda x: x["name"], response["response_map"]["entries"]))
        # Check if the project exist
        if sl_project in projects:
            print(f"\t- The project exists! -")
            return True
        else:
            print(f"\t- The project does not exists! -")
            return False
    elif response["http_status_code"] == 404:
        print(f"\t- The target project space {sl_pspace} does not exists! -")
        return False
    else:
        exit("# Invalid request - SnapLogic list projects endpoint! #")

def sl_check_project_space_existence(sl_org, sl_pspace, sl_auth):
    # This function checks if the given project space exists in SnapLogic.
    print(f"-- Checking the existence of project space: {sl_org}/{sl_pspace} --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/asset/list/{sl_org}"
    payload = {}
    response = requests.request("GET", url, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] == 200:
        project_spaces = list(map(lambda x: x["name"], response["response_map"]["entries"]))
        # Check if the project exist
        if sl_pspace in project_spaces:
            print(f"\t- The project space exists! -")
            return True
        else:
            print(f"\t- The project space does not exists! -")
            return False
    else:
        exit("# Invalid request - SnapLogic list project spaces endpoint! #")

def sl_create_project_space(sl_org, sl_pspace,sl_auth,):
    # This function creates project space in SnapLogic.
    print(f"-- Creating project space {sl_org}/{sl_pspace} --")
    # Structure request
    url = f"https://cdn.elastic.snaplogic.com/api/1/rest/asset/{sl_org}/{sl_pspace}"
    params = {
        "path":f"{sl_org}/{sl_pspace}"
    }
    payload = json.dumps({
        "asset_type": "Dir",
        "name": sl_pspace
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, params=params, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 200:
        exit("# Invalid request - SnapLogic create project space endpoint! #")
    print(f"\t- Created successfully! -")

def sl_list_assets(sl_org, sl_pspace, sl_project, sl_auth, asset_type):
    # This function list all of the assets by asset type in the given project.
    asset_print = "Task" if asset_type == "Job" else asset_type
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/asset/list/{sl_org}/{sl_pspace}/{sl_project}?asset_type={asset_type}"
    payload = {}
    response = requests.request("GET", url, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] == 200:
        return response["response_map"]["entries"]
    else:
        exit("# Invalid request - SnapLogic list assets endpoint! #")

def sl_filter_tracked_assets(assets):
    # This function filters only tracked assets.
    return list(filter(lambda x: "git" in x["metadata"],assets))
    
def sl_checkout_to_project(sl_org, sl_pspace, sl_project, sl_auth, gh_ref):
    # This function checksout from GitHub ref to SnapLogic project.
    print(f"-- Checking out project {sl_project} from {gh_ref}/test --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/public/project/checkout/{sl_org}/{sl_pspace}/{sl_project}"
    payload = json.dumps({
        "repo": gh_ref,
        "ref": "test",
        "hard_reset": True,
        "discard_untracked_file": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, auth=sl_auth, headers=headers, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 200:
        exit("# Invalid request - SnapLogic checkout project endpoint! #")
    print(f"\t- Checked out successfully! -")

def sl_checkout_to_project_tag(sl_org, sl_pspace, sl_project, sl_auth, gh_ref, tag_name):
    # This function checksout from GitHub tag to SnapLogic project.
    print(f"\t-- Checking out project {sl_project} from {gh_ref}/{tag_name} --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/public/project/checkout/{sl_org}/{sl_pspace}/{sl_project}"
    payload = json.dumps({
        "repo": gh_ref,
        "ref": tag_name,
        "hard_reset": True,
        "discard_untracked_file": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, auth=sl_auth, headers=headers, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 200:
        exit("# Invalid request - SnapLogic checkout project endpoint! #")
    print(f"\t\t- Checked out successfully! -")

def sl_create_project_by_checkout(sl_org, sl_pspace, sl_project, sl_auth, gh_ref):
    # This function creates project in SnapLogic by checkingout from GitHub ref.
    print(f"-- Creating project {sl_project} by checking out from {gh_ref}/test --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/public/project/create-project/{sl_org}/{sl_pspace}/{sl_project}"
    payload = json.dumps({
            "repo": gh_ref,
            "ref": "test"
        })
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 200:
        exit("# Invalid request - SnapLogic create project by checkout endpoint! #")
    print(f"\t- Created successfully! -")

def sl_create_project_by_checkout_tag(sl_org, sl_pspace, sl_project, sl_auth, gh_ref, tag_name):
    # This function creates project in SnapLogic by checkingout from GitHub tag.
    print(f"-- Creating project {sl_project} by checking out from {gh_ref}/{tag_name} --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/public/project/create-project/{sl_org}/{sl_pspace}/{sl_project}"
    payload = json.dumps({
            "repo": gh_ref,
            "ref": tag_name
        })
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=headers, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 200:
        exit("# Invalid request - SnapLogic create project by checkout endpoint! #")
    print(f"\t- Created successfully! -")

def sl_run_test_pipeline(sl_org, sl_pspace, sl_project, sl_test_pipeline, sl_auth):
    # This functions triggers SnapLogic Test Pipeline
    print(f"-- Triggering {sl_org}/{sl_pspace}/{sl_project}/{sl_test_pipeline} pipeline --")
    # Structure request
    url = f"https://elastic.snaplogic.com/api/1/rest/slsched/feed/{sl_org}/{sl_pspace}/{sl_project}/{sl_test_pipeline}"
    payload={}
    response = requests.request("GET", url, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 200:
        print(f"\t- Tests failed / SnapLogic bad request! -")
    else:
        print(f"\t- Test passed! -")

def gh_get_latest_release(gh_owner, gh_repo, gh_token):
    # This function retrieves the latest release for a give GitHub repository.
    # Structure request
    url = f"https://api.github.com/repos/{gh_owner}/{gh_repo}/releases/latest"
    payload={}
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {gh_token}"
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 200 and response.status_code != 404:
        exit("# Invalid request - GitHub get latest release endpoint! #")
    response = json.loads(response.text)
    return response.get("tag_name")

def gh_create_release(gh_owner, gh_repo, tag_name, gh_token):
    # This functions creates a new GitHub release tag.
    # Structure request
    url = f"https://api.github.com/repos/{gh_owner}/{gh_repo}/releases"
    payload = json.dumps({
        "tag_name":tag_name,
        "name":"Automated release CI/CD.",
        "body":"Automated release CI/CD."
    })
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {gh_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 201:
        exit("# Invalid request - GitHub create release endpoint! #")
    return tag_name

def pete_auth(pete_email, pete_pw, pete_key):
    # This functions retrieves authentication token for the IWDG Tool.
    # Structure request
    url = "https://iwdg-phase2-prod-fa.azurewebsites.net/api/user/login"
    payload = json.dumps({
        "user": pete_email,
        "password": pete_pw
    })
    headers = {
        "x-functions-key": pete_key,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 201:
        exit("# Invalid request - IWDG Authentication endpoint! #")
    else:
        response = json.loads(response.text)
        return response.get("accessToken")

def pete_generate_documentation(pete_key, pete_token, sl_org, sl_pspace, sl_project, pete_target_system, pete_main_page):
    # This function generates documentation using the PETE Tool.
    print(f"-- Genarting documenation. --")
    print(f"\tSLOrganization: {sl_org}\n\tSLProjectSpace: {sl_pspace}\n\tSLProject: {sl_project}\n\tPETEMainPage: {pete_main_page}")
    # Structure request
    url = "https://iwdg-phase2-prod-fa.azurewebsites.net/api/documentation"
    if pete_target_system == "Confluence":
        payload = pete_confluence_body(sl_org, sl_pspace, sl_project, pete_main_page)
    elif pete_target_system == "Sharepoint":
        payload = pete_sharepoint_body(sl_org, sl_pspace, sl_project, pete_main_page)
    else:
        payload = pete_pdf_body(sl_org, sl_pspace, sl_project)
    headers = {
        "Authorization": f"Bearer {pete_token}",
        "x-functions-key": pete_key,
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 201:
        exit("# Invalid request - IWDG Generate Documentation endpoint! #")
    else:
        response = json.loads(response.text)
        print(f"-- IWDG: {' - '.join(response)} --")

def pete_confluence_body(sl_org, sl_pspace, sl_project, pete_main_page):
    return json.dumps({
        "SLOrganization": sl_org,
        "SLProjectSpace": sl_pspace,
        "SLProject": sl_project,
        "ConfluenceMainPage": pete_main_page,
        "configFiles":[],
        "storePathOnly": False
    })

def pete_sharepoint_body(sl_org, sl_pspace, sl_project, pete_main_page):
    return json.dumps({
        "SLOrganization": sl_org,
        "SLProjectSpace": sl_pspace,
        "SLProject": sl_project,
        "SharepointMainPage": pete_main_page,
        "configFiles":[],
        "storePathOnly": False
    })

def pete_pdf_body(sl_org, sl_pspace, sl_project):
    return json.dumps({
        "SLOrganization": sl_org,
        "SLProjectSpace": sl_pspace,
        "SLProject": sl_project,
        "ConfluenceMainPage": "",
        "confluence_page_url": "",
        "configFiles":""
    })

def sl_get_task_details(sl_auth, snode_id):
    # This function retrieves details about given task.
    # Structure request
    url = f"https://cdn.elastic.snaplogic.com/api/1/rest/slsched/job/{snode_id}"
    payload = {}
    response = requests.request("GET", url, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] == 200:
        response = response["response_map"]
        return response
    else:
        exit("# Invalid request - SnapLogic get task details endpoint! #")

def sl_update_triggered_task(sl_org, sl_pspace, sl_project, sl_auth, task_details):
    # This function updates a SnapLogic triggered task.
    # Structure request
    url = f"https://cdn.elastic.snaplogic.com/api/1/rest/slsched/job/{task_details['snode_id']}"
    payload = json.dumps(task_details)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, auth=sl_auth, data=payload)
    response = json.loads(response.text)
    # Validate response
    if response["http_status_code"] != 201:
        exit("# Invalid request - SnapLogic update-task endpoint! #")
    print(f"\t- Triggered Task {sl_org}/{sl_pspace}/{sl_project}/{task_details['job_name']} successfully! -")

def gh_list_artifacts(gh_ref, gh_token):
    # This function lists all workflow artifacts in repository.
    # Structure request
    url = f"https://api.github.com/repos/{gh_ref}/actions/artifacts"
    payload={}
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {gh_token}"
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 200 and response.status_code != 404:
        exit("# Invalid request - GitHub get latest release endpoint! #")
    response = json.loads(response.text)
    return response

def gh_delete_artifact(gh_ref, gh_token, artifact_id):
    # This function deletes workflow artifact from GitHub repository.
    # Structure request
    url = f"https://api.github.com/repos/{gh_ref}/actions/artifacts/{artifact_id}"
    payload={}
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {gh_token}"
    }
    response = requests.request("DELETE", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 204 and response.status_code != 404:
        exit("# Invalid request - GitHub get latest release endpoint! #")
    print(f"\t - Artifact with ID - {artifact_id} has been deleted! -")

def gh_run_workflow(gh_ref, gh_token, workflow):
    # This function triggers the delete-artifacts workflow on main branch.
    # Structure request
    url = f"https://api.github.com/repos/{gh_ref}/actions/workflows/{workflow}/dispatches"
    payload = json.dumps({
        "ref": "main",
        "inputs": {}
    })
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {gh_token}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # Validate response
    if response.status_code != 204 and response.status_code != 404:
        print(response)
        exit("# Invalid request - GitHub get latest release endpoint! #")