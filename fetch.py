import requests
import os
import subprocess
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def list_repositories(github_username):
    url = f'https://api.github.com/users/{github_username}/repos'
    page = 1
    repositories = []

    while True:
        response = requests.get(url, params={'page': page, 'per_page': 100})
        
        if response.status_code != 200:
            console.print(f"[red]Error fetching repositories: {response.status_code}[/red]")
            break
        
        repos = response.json()
        if not repos:
            break
        
        repositories.extend(repos)
        page += 1

    return repositories

def display_repositories(repositories):
    console.print("\n[bold cyan]GitHub Repositories:[/bold cyan]")
    table = Table(title="Available Repositories", title_justify="center")
    table.add_column("ID", justify="center", style="bold magenta")
    table.add_column("Name", justify="left", style="bold green")
    table.add_column("URL", justify="left", style="blue")

    for i, repo in enumerate(repositories):
        table.add_row(str(i + 1), repo['name'], repo['html_url'])

    console.print(table)

def view_repository_details(repo):
    console.print(f"\n[bold yellow]Repository Details:[/bold yellow]")
    console.print(f"[green]Name:[/green] {repo['name']}")
    console.print(f"[green]Description:[/green] {repo.get('description', 'No description available.')}")
    console.print(f"[green]URL:[/green] {repo['html_url']}")
    console.print(f"[green]Clone URL:[/green] {repo['clone_url']}")
    console.print(f"[green]Language:[/green] {repo.get('language', 'N/A')}")
    console.print(f"[green]Stars:[/green] {repo['stargazers_count']}")
    console.print(f"[green]Forks:[/green] {repo['forks_count']}")
    console.print(f"[green]Open Issues:[/green] {repo['open_issues_count']}\n")

def clone_repository(repo_url, target_directory):
    console.print(f"[blue]Cloning {repo_url} into {target_directory}...[/blue]")
    result = subprocess.run(["git", "clone", repo_url, target_directory])
    if result.returncode == 0:
        console.print(f"[green]Successfully cloned into {target_directory}.[/green]")
    else:
        console.print(f"[red]Failed to clone repository.[/red]")

def clone_all_repositories(repositories, target_directory):
    for repo in repositories:
        repo_name = repo['name']
        clone_directory = os.path.join(target_directory, repo_name)
        clone_repository(repo['clone_url'], clone_directory)

def main():
    console.print("[bold cyan]Welcome to GitHub Repository Manager[/bold cyan]")
    console.print("[bold red]Made by github.com/Cr0mb/[/bold red]")
    github_username = Prompt.ask("Enter the GitHub username")
    repositories = list_repositories(github_username)

    if not repositories:
        console.print("[yellow]No repositories found.[/yellow]")
        return

    display_repositories(repositories)

    while True:
        choice = Prompt.ask("Choose an option:\n1. View details about a given repository\n2. Download Repository\n3. Download All Repositories\n4. Exit", default="4")

        if choice == '1':
            repo_number = Prompt.ask("Enter the repository number to view details")
            try:
                repo_index = int(repo_number) - 1
                if 0 <= repo_index < len(repositories):
                    view_repository_details(repositories[repo_index])
                else:
                    console.print("[red]Invalid repository number.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")

        elif choice == '2':
            repo_number = Prompt.ask("Enter the repository number to download")
            try:
                repo_index = int(repo_number) - 1
                if 0 <= repo_index < len(repositories):
                    target_directory = Prompt.ask("Enter the directory to download the repository to")

                    if not os.path.exists(target_directory):
                        os.makedirs(target_directory)

                    clone_repository(repositories[repo_index]['clone_url'], os.path.join(target_directory, repositories[repo_index]['name']))
                else:
                    console.print("[red]Invalid repository number.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")

        elif choice == '3':
            target_directory = Prompt.ask("Enter the directory to download all repositories to")

            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

            clone_all_repositories(repositories, target_directory)

        elif choice == '4':
            console.print("[yellow]Exiting...[/yellow]")
            break

        else:
            console.print("[red]Invalid choice. Please select 1, 2, 3, or 4.[/red]")

if __name__ == '__main__':
    main()
