from collections import defaultdict

import requests
import matplotlib.pyplot as plt
import sys

import json


# ------------------------
# Data Gathering
# ------------------------

def fetch_new_langs(username: str, token : str=None):
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

def load_from_json(path):
    if path:
        with open(path, 'r') as f:
            data = json.load(f)
        # force counts to ints
        return {lang: int(count) for lang, count in data.items()}
    return {}

# ------------------------
# Centralized Processing
# ------------------------

def process_lang_data(lang_data: dict, min_pct: float = 0.015, color_file="lang_colors.json"):
    if not lang_data:
        raise ValueError("No language data found.")

    total_bytes = sum(lang_data.values())
    major = []
    minor_total = 0
    colors = []

    with open(color_file, "r") as f:
        color_data = json.load(f)

    for lang, count in lang_data.items():
        if count / total_bytes >= min_pct:
            major.append((lang, count))
            colors.append(color_data.get(lang, {}).get("color", "#999999"))
        else:
            minor_total += count

    if minor_total > 0:
        major.append(("Other", minor_total))
        colors.append("#000000")

    sizes = [count for _, count in major]
    labels = [lang for lang, _ in major]
    percentages = [f"{lang} - {count / total_bytes:.1%}" for lang, count in major]

    return {
        "sizes": sizes,
        "labels": labels,
        "colors": colors,
        "percentages": percentages,
        "total": total_bytes,
    }

# ------------------------
# Chart Renderers
# ------------------------

def create_pie_chart(username: str, lang_data: dict, min_pct):
    processed = process_lang_data(lang_data, min_pct)

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, _ = ax.pie(processed["sizes"], colors=processed["colors"])

    ax.legend(
        wedges,
        processed["percentages"],
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    ax.set_title(f"{username}'s Most Used Languages")
    ax.axis("equal")
    fig.tight_layout()
    return fig, ax

# ------------------------
# Utilites
# ------------------------

def save_chart_to_file(fig, path: str, dpi: int = 300):
    fig.savefig(path, bbox_inches="tight", dpi=dpi)
    plt.close(fig)
    print(f"[LOG] Chart Saved to {path}")

def show_chart(fig):
    # display chart
    fig.show()


# ------------------------
# Main
# ------------------------

if __name__ == "__main__":

    print("[LOG] Starting Script. See README for Settings Help")

    with open("settings.json", 'r') as f:
        settings = json.load(f)

    print("[LOG] Reading Settings")

    username = settings["username"]
    token = settings["token"]

    chart_save_path = settings["json_save_path"]
    lang_data = defaultdict(int)

    print("[LOG] Fetching Language Data")

    if settings["use_data"] == "new":
        print("[LOG] Getting New Data")
        lang_data = fetch_new_langs(username,token)
    elif settings["use_data"] == "old":
        print("[LOG] Using Old Data")
        lang_data = load_from_json(chart_save_path)
    else:
        print("[LOG/ERROR] Invalid Data Selection (use_data)")

    print("[LOG] Creating Chart")
    minimum_percentage = settings["minimum_percentage"]
    fig, ax = create_pie_chart(username, lang_data, minimum_percentage)

    output_option = settings["output_option"]
    if output_option == "save":
        print("[LOG] Saving Chart")
        image_save_path = settings["image_save_path"]
        save_chart_to_file(fig, image_save_path)
    elif output_option == "show":
        print("[LOG] Showing Chart")
        show_chart(fig)
    else:
        print("[LOG/ERROR] Invalid Output Type (output_option)")