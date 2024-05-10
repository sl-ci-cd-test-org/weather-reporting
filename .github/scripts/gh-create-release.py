import sys
from helpers import *

#Arguments send by position:
    # 0.script_name
    # 1.gh_ref
    # 2.gh_token

if __name__ == "__main__":
   
    # Capture arguments
    gh_ref = sys.argv[1]
    gh_token = sys.argv[2]
    gh_owner = gh_ref.split("/")[0]
    gh_repo = gh_ref.split("/")[1]

    # Print arguments
    print(f"""-- Command line arguments--
        gh_token: {gh_token}
        gh_ref: {gh_ref}
        gh_owner: {gh_owner}
        gh_repo: {gh_repo}""")
    
    # Get latest release
    tag_name = gh_get_latest_release(gh_owner, gh_repo, gh_token)

    # Check if there is a release
    if tag_name != None:
        # Create incremental release
        tag_name = tag_name[:1] + str(float(tag_name[1:]) + 1)
        print(f"-- New release - {tag_name} --")
        print(f"\t- Proceeding with release creation -")
        release_created = gh_create_release(gh_owner, gh_repo, tag_name, gh_token)
        print(f"\t\t # Release created? - {release_created} #")
    else:
        # Create initial release
        print("-- There are no releases --")
        print(f"-- New release - v1.0 --")
        print(f"\t- Proceeding with release creation -")
        release_created = gh_create_release(gh_owner, gh_repo, "v1.0", gh_token)
        print(f"\t\t # Release created? - {release_created} #")