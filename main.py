import os
import subprocess
import random
from datetime import datetime, timedelta
from pathlib import Path

def create_past_commits(start_date):
    repo_path = Path(__file__).resolve().parent

    os.chdir(repo_path)
    
    try:
        subprocess.run(["git", "status"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: The specified path is not a valid Git repository.")
        return
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    today = datetime.now()
    
    # Initialize a single file
    file_name = repo_path / "single_file.txt"
    with file_name.open("w") as f:
        f.write("Initial content\n")
    
    # Stage all changes to handle deletions and untracked files
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    
    current_date = start_date
    while current_date <= today:
        num_commits = random.randint(1, 24)  # Number of commits for this date
        
        for _ in range(num_commits):
            with file_name.open("a") as f:
                f.write(f"Update on {current_date.strftime('%Y-%m-%d')} at commit {_ + 1}\n")
            
            # Stage all changes, including the updated file
            subprocess.run(["git", "add", "-A"], check=True)
            
            commit_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = commit_date_str
            env["GIT_COMMITTER_DATE"] = commit_date_str
            
            commit_message = f"Update on {current_date.strftime('%Y-%m-%d')} commit {_ + 1}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True, env=env)
            
            print(f"Created commit {_ + 1} for {current_date.strftime('%Y-%m-%d')}")
        
        current_date += timedelta(days=1)
    
    try:
        subprocess.run(["git", "push"], check=True)
        print("All commits pushed to the remote repository successfully.")
    except subprocess.CalledProcessError:
        print("Error: Failed to push commits to the remote repository.")

if __name__ == "__main__":

    start_date = "2024-01-20"
    
    create_past_commits(start_date)
