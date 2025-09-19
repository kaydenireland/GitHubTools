from collections import defaultdict
import requests
import matplotlib.pyplot as plt
import json
import sys


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

def save_to_json(lang_data: dict):
    file_name = "output.json"

    with open(file_name, 'w') as f:
        json.dump(lang_data, f, indent=4)

def load_from_json(path: str):
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

def create_pie_chart(username: str, lang_data: dict, min_pct: float):
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

def create_donut_chart(username: str, lang_data: dict, min_pct: float, dh_width: float):
    processed = process_lang_data(lang_data, min_pct)

    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, _ = ax.pie(
        processed["sizes"],
        colors=processed["colors"],
        wedgeprops=dict(width=dh_width)  # donut hole
    ) # TODO setting for donut hole width

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


def create_bar_chart(username: str, lang_data: dict, min_pct: float):
    processed = process_lang_data(lang_data, min_pct)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(processed["labels"], processed["sizes"], color=processed["colors"])
    ax.set_xlabel("Bytes of Code")
    ax.set_title(f"{username}'s Most Used Languages")
    fig.tight_layout()
    return fig, ax

# ------------------------
# Save/Show
# ------------------------

def save_chart_to_file(fig, path: str, dpi: int = 300):
    fig.savefig(path, bbox_inches="tight", dpi=dpi)
    plt.close(fig)
    print(f"[LOG] Chart Saved to {path}")

def show_chart(fig):
    # display chart
    fig.show()


# ------------------------
# Factory
# ------------------------

def get_lang_data(use_data: str, username: str, token: str, chart_save_path: str):
    lang_data = defaultdict(int)

    if use_data == "new":
        print("[LOG] Getting New Data")
        lang_data = fetch_new_langs(username, token)
    elif use_data == "old":
        print("[LOG] Using Old Data")
        lang_data = load_from_json(chart_save_path)
    else:
        print("[LOG/ERROR] Invalid Data Selection (use_data)")
    return lang_data

def create_chart(type: str, username: str, lang_data: dict, minimum_percentage: float, dh_width: float):
    if type == "pie":
        fig, ax = create_pie_chart(username, lang_data, minimum_percentage)
    elif type == "donut":
        fig, ax = create_donut_chart(username, lang_data, minimum_percentage, dh_width)
    elif type == "bar":
        fig, ax = create_bar_chart(username, lang_data, minimum_percentage)
    else:
        print("[LOG/ERROR] Invalid Chart Type (chart_type)")
        return
    return fig, ax

def output_chart(output_option: str, image_save_path: str, fig):
    if output_option == "save":
        print("[LOG] Saving Chart")
        save_chart_to_file(fig, image_save_path)
    elif output_option == "show":
        print("[LOG] Showing Chart")
        show_chart(fig)
    else:
        print("[LOG/ERROR] Invalid Output Type (output_option)")

def run():
    print("[LOG] Starting Script. See README for Settings Help")
    with open("settings.json", 'r') as f:
        settings = json.load(f)

    '''
    Gather All Settings
    '''
    print("[LOG] Reading Settings")
    username_setting = settings["username"]
    token_setting = settings["token"]
    chart_save_path_setting = settings["json_save_path"]
    use_data_setting = settings["use_data"]
    minimum_percentage_setting = settings["minimum_percentage"]
    chart_type_setting = settings["chart_type"]
    donut_hole_width_setting = settings["donut_hole_width"]
    output_option_setting = settings["output_option"]
    image_save_path_setting = settings["image_save_path"]

    print("[LOG] Fetching Language Data")
    lang_data = get_lang_data(use_data_setting, username_setting, token_setting, chart_save_path_setting)

    print("[LOG] Creating Chart")
    fig, ax = create_chart(chart_type_setting, username_setting, lang_data, minimum_percentage_setting, donut_hole_width_setting)

    print("[LOG] Sharing Chart")
    output_chart(output_option_setting, image_save_path_setting, fig)


# ------------------------
# Main
# ------------------------

if __name__ == "__main__":
    run()
# TODO better documentation, comment entire program