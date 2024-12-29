import os
import sys
from github import Github

def main():
    # Get the GitHub token from environment variables
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN is not set")
        sys.exit(1)

    # Get the GitHub repository and pull request info from environment variables
    repo_name = os.getenv("GITHUB_REPOSITORY")
    if not repo_name:
        print("GITHUB_REPOSITORY is not set")
        sys.exit(1)

    pr_number = os.getenv("GITHUB_REF").split("/")[-1]
    if not pr_number.isdigit():
        print("Invalid pull request number")
        sys.exit(1)

    pr_number = int(pr_number)

    # Connect to the GitHub API
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Get the pull request
    pr = repo.get_pull(pr_number)

    # Get the list of files changed in the pull request
    changed_files = pr.get_files()
    flagged_files = []

    for file in changed_files:
        # Ensure we only check text-based files (non-binary)
        if file.patch:  # Only files with a patch (diff) are text-based
            if "secret" in file.patch:
                flagged_files.append(file.filename)
    
    if flagged_files:
        print("The following files contain the word 'secret':")
        for file in flagged_files:
            print(f"- {file}")
        sys.exit(1)  # Fail the action if "secret" is found

    print("No files contain the word 'secret'.")
    sys.exit(0)


if __name__ == "__main__":
    main()
