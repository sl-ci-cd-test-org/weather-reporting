import sys
from helpers import *

#Arguments send by position:
    # 0.script_name
    # 1.pete_email
    # 2.pete_pw
    # 3.pete_key
    # 4.sl_target_org
    # 5.sl_target_pspace
    # 6.sl_project
    # 7.pete_target_system
    # 8.pete_main_page

if __name__ == "__main__":
   
    # Capture arguments
    pete_email = sys.argv[1]
    pete_pw = sys.argv[2]
    pete_key = sys.argv[3]
    sl_target_org = sys.argv[4]
    sl_target_pspace = sys.argv[5]
    sl_project = sys.argv[6]
    pete_target_system = sys.argv[7]
    pete_main_page = sys.argv[8]

    # Print arguments
    print(f"""-- Command line arguments --
        pete_email: {pete_email}
        pete_pw: {pete_pw}
        pete_key: {pete_key}
        sl_target_org: {sl_target_org}
        sl_target_pspace: {sl_target_pspace}
        sl_project: {sl_project}
        pete_target_system: {pete_target_system}
        pete_main_page: {pete_main_page}""")
    
    # Authenticate PETE
    pete_token = pete_auth(pete_email, pete_pw, pete_key)

    # Upsert PETE documentation
    pete_generate_documentation(pete_key, pete_token, sl_target_org, sl_target_pspace, sl_project, pete_target_system, pete_main_page)