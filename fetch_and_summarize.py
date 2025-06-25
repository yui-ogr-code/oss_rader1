import os
import requests
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

GITHUB_API = "https://api.github.com/search/repositories"
HEADERS = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}

def fetch_top_repos():
    params = {
        "q": "stars:>10000",
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }
    r = requests.get(GITHUB_API, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json().get("items", [])

def summarize_repo(repo):
    text = f"リポジトリ名: {repo['full_name']}\n説明: {repo['description']}\n更新: {repo['updated_at']}\n"
    prompt = f"以下のリポジトリ情報を簡潔に日本語で要約してください:\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()

def main():
    repos = fetch_top_repos()
    md_lines = ["# 人気OSSリポジトリ更新まとめ\n"]
    for repo in repos:
        summary = summarize_repo(repo)
        md_lines.append(f"## {repo['full_name']}\n")
        md_lines.append(f"{summary}\n\n")

    with open("site/content/summary.md", "w", encoding="utf-8") as f:
        f.writelines(line + "\n" for line in md_lines)

if __name__ == "__main__":
    main()
