# Import libraries
import sys
from requests.auth import HTTPBasicAuth
import json
from helpers import *

#Arguments send by position:
    # 0.script_name
    # 1.sl_email
    # 2.sl_pw
    # 3.sl_target_org
    # 4.sl_target_pspace
    # 5.sl_target_project
    # 6.gh_ref

if __name__ == "__main__":
   
    # Capture arguments
    sl_email = sys.argv[1]
    sl_pw = sys.argv[2]
    sl_target_org = sys.argv[3]
    sl_target_pspace = sys.argv[4]
    sl_target_project = sys.argv[5]
    gh_ref = sys.argv[6]
    sl_auth= HTTPBasicAuth(sl_email, sl_pw)

    # Print arguments
    print(f"""-- Command line arguments --
        sl_email: {sl_email}
        sl_pw: {sl_pw}
        sl_target_org: {sl_target_org}
        sl_target_pspace: {sl_target_pspace}
        sl_project: {sl_target_project}
        gh_ref: {gh_ref}""")
    
    # Check if target project space exists, if not create.
    if not sl_check_project_space_existence(sl_target_org, sl_target_pspace, sl_auth):
        sl_create_project_space(sl_target_org, sl_target_pspace, sl_auth)

    # Check if target project exists in SnapLogic
    if sl_check_project_existence(sl_target_org, sl_target_pspace, sl_target_project, sl_auth):
        # If project exists preceed with checkout
        sl_checkout_to_project(sl_target_org, sl_target_pspace, sl_target_project, sl_auth, gh_ref)
    else:
        # If project doesn't exist preceed with create by checkout
        sl_create_project_by_checkout(sl_target_org, sl_target_pspace, sl_target_project, sl_auth, gh_ref)