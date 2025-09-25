from bs4 import BeautifulSoup
import requests

import json



# ------------------------
# Data Class
# ------------------------

class Repository:
    def __init__(self, name, author, language, star_count):
        self.name = name
        self.author = author
        self.language = language
        self.star_count = star_count

    def to_dict(self):
        return {
            "name": self.name,
            "author": self.author,
            "language": self.language,
            "star_count": self.star_count
        }

    def to_string(self):
        return self.name + "/" + self.author

    def get(self):
        return f"{self.to_string()}: {self.language}  *{self.star_count}"

# ------------------------
# Data Gathering
# ------------------------

def get_repos(language: str=""):

    base_url = "https://github.com/trending"
    url = f"{base_url}/{language}" if language else base_url
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to Load Trending Page: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    repos = []

    for repo in soup.find_all("article", class_ = "Box-row"):
        name = repo.h2.a.get_text(strip=True).replace(" ", "")
        name, author = name.split("/")

        stars_tag = repo.find("a", href=lambda x: x and x.endswith("/stargazers"))
        stars = stars_tag.get_text(strip=True) if stars_tag else "0"

        lang_tag = repo.find("span", itemprop="programmingLanguage")
        language = lang_tag.get_text(strip=True) if lang_tag else "Unknown"

        repo = Repository(name, author, language, stars)
        repos.append(repo)
    return repos


# ------------------------
# Data Output
# ------------------------

def print_output(repos):
    for repo in repos:
        print(repo.get())

def write_to_file(repos):
    with open("output.txt", "w") as fw:
        for repo in repos:
            fw.write(f"{repo.get()} \n")

def save_to_json(repos):
    file_name = "output.json"

    with open(file_name, 'w') as f:
        json.dump([repo.to_dict() for repo in repos], f, indent=4)



# ------------------------
# Factory
# ------------------------

def run():
    output = "save_json"

    lang = input("Enter language (skip for all): ").strip().lower()
    repos = get_repos(lang)

    if output == "print":
        print_output(repos)
    elif output == "save_json":
        save_to_json(repos)
    elif output == "save_txt":
        write_to_file(repos)



# ------------------------
# Main
# ------------------------

if __name__ == "__main__":
    run()