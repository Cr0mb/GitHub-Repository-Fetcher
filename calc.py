import requests
import os
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, Label
from rich.console import Console
from threading import Thread

console = Console()

class GitHubRepoManager:
    def __init__(self, root):
        self.root = root
        self.repositories = []
        self.repo_checkboxes = {}
        self.appearance_mode = "System"
        self.setup_ui()

    def setup_ui(self):
        self.root.title("GitHub Repository Manager")
        self.root.geometry("600x550")
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.root, text="GitHub Username:").pack(pady=10)
        self.username_entry = ctk.CTkEntry(self.root, width=300, placeholder_text="Enter GitHub username")
        self.username_entry.pack(pady=5)

        ctk.CTkButton(self.root, text="Fetch Repositories", command=self.fetch_repositories).pack(pady=5)

        self.repo_frame = ctk.CTkScrollableFrame(self.root, width=500, height=300)
        self.repo_frame.pack(pady=10, fill="both", expand=True)

        ctk.CTkButton(self.root, text="Clone Selected Repositories", command=self.clone_selected_repos).pack(pady=5)
        ctk.CTkButton(self.root, text="Clone All Repositories", command=self.clone_all_repos).pack(pady=5)

        ctk.CTkButton(self.root, text="🌓", width=50, height=30, command=self.toggle_mode).place(relx=0.95, rely=0.95, anchor="se")

    def fetch_repositories(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a GitHub username.")
            return

        self.clear_repository_checkboxes()
        Thread(target=self.list_repositories, args=(username,)).start()

    def clear_repository_checkboxes(self):
        self.repo_checkboxes.clear()
        for widget in self.repo_frame.winfo_children():
            widget.destroy()
        self.repositories = []

    def list_repositories(self, github_username):
        url = f'https://api.github.com/users/{github_username}/repos'
        page = 1

        while True:
            response = requests.get(url, params={'page': page, 'per_page': 100})
            if response.status_code != 200:
                messagebox.showerror("Error", f"Failed to fetch repositories: {response.status_code}")
                break

            repos = response.json()
            if not repos:
                break

            self.repositories.extend(repos)
            self.create_repo_checkboxes(repos)
            page += 1

    def create_repo_checkboxes(self, repos):
        for repo in repos:
            self.create_repo_checkbox(repo)

    def create_repo_checkbox(self, repo):
        repo_frame = ctk.CTkFrame(self.repo_frame)
        repo_frame.pack(fill="x", pady=2)

        var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(repo_frame, text=repo['name'], variable=var)
        checkbox.pack(side="left", padx=5)
        self.repo_checkboxes[repo['name']] = var

        details_btn = ctk.CTkButton(repo_frame, text="Details", width=80,
                                     command=lambda r=repo: self.show_repo_details(r))
        details_btn.pack(side="right", padx=5)

    def clone_selected_repos(self):
        selected_repos = [repo for repo, var in self.repo_checkboxes.items() if var.get()]

        if not selected_repos:
            messagebox.showwarning("Warning", "Please select at least one repository to clone.")
            return

        target_directory = filedialog.askdirectory(title="Select Directory to Clone Repositories Into")
        if not target_directory:
            return

        Thread(target=self.clone_repositories, args=(selected_repos, target_directory)).start()

    def clone_repositories(self, selected_repos, target_directory):
        for repo in self.repositories:
            if repo['name'] in selected_repos:
                self.clone_repository(repo['clone_url'], os.path.join(target_directory, repo['name']))

    def clone_repository(self, repo_url, target_directory):
        console.print(f"Cloning {repo_url} into {target_directory}...")
        result = subprocess.run(["git", "clone", repo_url, target_directory], capture_output=True)
        if result.returncode == 0:
            console.print(f"Successfully cloned into {target_directory}")
        else:
            console.print(f"Failed to clone repository:\n{result.stderr.decode()}")


    def clone_all_repos(self):
        target_directory = filedialog.askdirectory(title="Select Directory to Clone All Repos Into")
        if not target_directory:
            return

        Thread(target=self.clone_repositories, args=([repo['name'] for repo in self.repositories], target_directory)).start()

    def toggle_mode(self):
        self.appearance_mode = "Dark" if self.appearance_mode == "Light" else "Light"
        ctk.set_appearance_mode(self.appearance_mode)

    def show_repo_details(self, repo):
        details_window = Toplevel(self.root)
        details_window.title(f"Details for {repo['name']}")
        details_window.geometry("400x300")

        labels = [
            f"Repository: {repo['name']}",
            f"Description: {repo['description'] or 'No description available.'}",
            f"Stars: {repo['stargazers_count']}",
            f"Forks: {repo['forks_count']}",
            f"Language: {repo['language'] or 'Not specified.'}",
            f"URL: {repo['html_url']}",
        ]
        
        for text in labels:
            Label(details_window, text=text, wraplength=350, justify="left", font=("Arial", 12)).pack(pady=5)

def main():
    root = ctk.CTk()
    app = GitHubRepoManager(root)
    root.mainloop()

if __name__ == '__main__':
    main()
