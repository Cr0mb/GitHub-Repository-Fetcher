import requests
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

def display_titles():
    title = pyfiglet.figlet_format("GitHub Fetcher", font="slant")
    co_title = "Made by Cr0mb"
    print(Fore.CYAN + title + Style.RESET_ALL)
    print(Fore.RED + co_title + Style.RESET_ALL + "\n")

def get_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        repos = response.json()

        print(Fore.CYAN + f'Repositories for {username}:\n' + Style.BRIGHT)
        for repo in repos:
            title = repo.get('name')
            description = repo.get('description') or 'No description available'
            print(Fore.GREEN + f'Title: {title}')
            print(Fore.YELLOW + f'Description: {description}\n' + Style.RESET_ALL)
    
    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + f'HTTP error occurred: {http_err}' + Style.RESET_ALL)
    except Exception as err:
        print(Fore.RED + f'An error occurred: {err}' + Style.RESET_ALL)

def main():
    display_titles()
    username = input(Fore.MAGENTA + "Enter the GitHub username: " + Style.RESET_ALL)
    get_repositories(username)

if __name__ == "__main__":
    main()
