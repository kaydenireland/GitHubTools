from collections import defaultdict

import requests
import matplotlib as plt
import sys

import json

from matplotlib.font_manager import json_dump


def fetch_langs(username: str, token : str=None):
    headers = {"Authorization": f"token {token}"} if token else {}
    lang_totals = defaultdict(int)
    page = 1

    while True:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"

        repos = requests.get(repos_url, headers=headers).json()
        if isinstance(repos, dict) and repos.get("message"):
            raise Exception(f"Error fetching repos: {repos['message']}")
        if not repos:
            break # if there are no remaining repos

        for repo in repos:
            langs_url = repo["languages_url"]
            langs = requests.get(langs_url, headers=headers).json()
            for lang, count in langs.items():
                lang_totals[lang] += count

        page += 1

    return dict(sorted(lang_totals.items(), key=lambda x: x[1], reverse=True))


def save_to_json(lang_data):
    file_name = "output.json"

    #json_str = json.dumps(lang_data, indent=4)
    with open(file_name, 'w') as f:
        #f.write(json_str)
        json.dump(lang_data, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <github-username> [github-token]")
        sys.exit(1)

    username = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None

    lang_data = (fetch_langs(username, token))
    save_to_json(lang_data)