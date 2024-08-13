import os
import subprocess
from dotenv import load_dotenv

TOKEN_GITHUB = os.getenv('TOKEN_GITHUB', '')
USER = "MoeKernel"
REPO = "android_kernel_xiaomi_ginkgo"

def run_command(command):
    """Executes a shell command and returns the output."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.stdout:
        return result.stdout.strip()
    if result.stderr:
        return result.stderr.strip()
    return None

def clone_repo():
    """Clones the kernel repository."""
    remote_url = f'https://{USER}:{TOKEN_GITHUB}@github.com/{USER}/{REPO}.git'
    if not os.path.exists(REPO):
        result = run_command(f"git clone {remote_url}")
        print(result)
    else:
        print(f"The repository {REPO} has already been cloned.")

def fetch_and_reset_upstream(upstream_repo, branch):
    """Fetches updates from the upstream repository and applies them to the current branch."""
    run_command(f"git remote add upstream {upstream_repo} || true")
    run_command(f"git fetch upstream {branch}")
    run_command(f"git reset --hard upstream/linux-4.14.y")

def merge_with_strategy(branch, file_specific_strategy=None):
    """Merges the upstream branch with the specified strategy."""
    result = run_command(f"git merge -X ours upstream/{branch}")

    if result and "CONFLICT" in result:
        print("Conflicts detected. Resolving automatically...")

        if file_specific_strategy:
            for file, strategy in file_specific_strategy.items():
                if file in run_command("git diff --name-only --diff-filter=U"):
                    print(f"Conflict detected in {file}. Using strategy '{strategy}'.")
                    run_command(f"git checkout --{strategy} {file}")
                    run_command(f"git add {file}")

        unmerged_files = run_command("git diff --name-only --diff-filter=U")
        if unmerged_files:
            unmerged_files_list = set(unmerged_files.splitlines())
            for file in unmerged_files_list:
                run_command(f"git add {file}")

        run_command("git commit -m 'Resolve merge conflicts: preserving local changes'")
        print("Conflicts resolved.")

    print(f"Merge of upstream changes from {branch} completed successfully.")

def clean_and_commit_makefile():
    """Removes the '-openela' part from the EXTRAVERSION variable in the Makefile and commits the changes."""
    try:
        with open('Makefile', 'r') as file:
            lines = file.readlines()

        modified = False
        with open('Makefile', 'w') as file:
            for line in lines:
                if line.startswith("EXTRAVERSION"):
                    if '-openela' in line:
                        line = "EXTRAVERSION =\n"
                        modified = True
                file.write(line)

        if modified:
            print("Makefile updated. Committing changes...")
            run_command("git add Makefile")
            run_command('git commit -m "Remove -openela from EXTRAVERSION in Makefile"')
            print("Changes to the Makefile committed successfully.")
        else:
            print("No changes needed in the Makefile.")
    except FileNotFoundError:
        print("Makefile not found. Please check if the file is present.")

def push_changes(branch):
    """Pushes the changes to the original repository."""
    remote_url = f'https://{USER}:{TOKEN_GITHUB}@github.com/{USER}/{REPO}.git'
    subprocess.run(["git", "remote", "set-url", "origin", remote_url])
    subprocess.run(["git", "config", "--global", "user.email", "akariondev@gmail.com"])
    subprocess.run(["git", "config", "--global", "user.name", "Akari Shoiya"])

    result = run_command(f"git push origin {branch}")
    if result:
        print(f"Pushed changes to branch {branch} successfully.")
    else:
        print(f"Failed to push changes to branch {branch}.")

def process_branches(upstream_repo, upstream_branch, branches):
    """Processes a list of branches to update and push changes."""
    fetch_and_reset_upstream(upstream_repo, upstream_branch)

    for branch in branches:
        print(f"Processing branch {branch}...")
        run_command(f"git checkout {branch}")
        merge_with_strategy(upstream_branch, file_specific_strategy={"Makefile": "theirs"})
        clean_and_commit_makefile()
        push_changes(branch)

if __name__ == "__main__":
    upstream_repo = "https://github.com/openela/kernel-lts.git"
    upstream_branch = "linux-4.14.y"
    branches = [
        "fourteen",
        "fourteen_dynamic_noksu",
        "fourteen_dynamic",
        "without-ksu",
        "openela"
    ]

    clone_repo()
    os.chdir(REPO)
    process_branches(upstream_repo, upstream_branch, branches)
