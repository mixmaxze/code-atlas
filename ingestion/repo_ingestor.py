from git import Repo
import os

class RepoIngestor:

    def __init__(self, repo_url, local_path="repos"):
        self.repo_url = repo_url
        self.local_path = local_path
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.repo_path = os.path.join(local_path, self.repo_name)

    def clone_repo(self):
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        if not os.path.exists(self.repo_path):
            print(f"Cloning repository {self.repo_url}...")
            Repo.clone_from(self.repo_url, self.repo_path)
        else:
            print("Repository already cloned.")

        return self.repo_path
    
def list_code_files(repo_path):

    code_extensions = [
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".c",
        ".go",
        ".rs"
    ]

    code_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                full_path = os.path.join(root, file)
                code_files.append(full_path)

    return code_files
