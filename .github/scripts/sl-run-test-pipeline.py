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
    # 5.sl_project
    # 6.sl_test_pipeline

if __name__ == "__main__":
   
    # Capture arguments
    sl_email = sys.argv[1]
    sl_pw = sys.argv[2]
    sl_target_org = sys.argv[3]
    sl_target_pspace = sys.argv[4]
    sl_project = sys.argv[5]
    sl_test_pipeline = sys.argv[6]
    sl_auth= HTTPBasicAuth(sl_email, sl_pw)

    # Print arguments
    print(f"""-- Command line arguments --
        sl_email: {sl_email}
        sl_pw: {sl_pw}
        sl_target_org: {sl_target_org}
        sl_target_pspace: {sl_target_pspace}
        sl_project: {sl_project}
        sl_test_pipeline: {sl_test_pipeline}""")
    
    # Trigger SnapLogic test pipeline
    sl_run_test_pipeline(sl_target_org, sl_target_pspace, sl_project, sl_test_pipeline, sl_auth)