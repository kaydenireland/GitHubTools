from collections import defaultdict

import requests
import matplotlib as plt
import sys

import json

from matplotlib.font_manager import json_dump


def fetch_langs(username: str, token : str=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"

    repos = requests.get(repos_url, headers=headers).json()
    if isinstance(repos, dict) and repos.get("message"):
        raise Exception(f"Error fetching repos: {repos['message']}")

    lang_totals = defaultdict(int)

    for repo in repos:
        langs_url = repo["languages_url"]
        langs = requests.get(langs_url, headers=headers).json()
        for lang, count in langs.items():
            lang_totals[lang] += count

    return lang_totals

def save_to_json(lang_data):
    file_name = "output.json"

    json_str = json.dumps(lang_data, indent=4)
    with open(file_name, 'w') as f:
        f.write(json_str)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <github-username> [github-token]")
        sys.exit(1)

    username = sys.argv[1]
    token = sys.argv[2] if sys.argv[2] else None

    lang_data = (fetch_langs(username, token))
    save_to_json(lang_data)