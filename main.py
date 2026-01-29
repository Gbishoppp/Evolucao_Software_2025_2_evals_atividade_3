import requests

OWNER = "openai"
REPO = "evals"

BASE_URL = "https://api.github.com"


def get_workflows():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/actions/workflows"
    response = requests.get(url)
    return response.json()


def get_workflow_file(path):
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    response = requests.get(url, headers=headers)
    return response.text


def analyze_workflow(content):
    result = {
        "test": False,
        "lint": False,
        "build": False,
        "docker": False,
        "deploy": False
    }

    keywords = {
        "test": ["pytest", "test", "eval"],
        "lint": ["flake8", "eslint", "lint"],
        "build": ["build", "compile"],
        "docker": ["docker", "container"],
        "deploy": ["deploy", "release"]
    }

    text = content.lower()

    for key in result:
        for word in keywords[key]:
            if word in text:
                result[key] = True

    return result


def main():
    print("🔍 Analisando repositório:", OWNER + "/" + REPO)
    print("-" * 50)

    data = get_workflows()

    if "workflows" not in data:
        print("Nenhum workflow encontrado.")
        return

    for wf in data["workflows"]:
        name = wf["name"]
        path = wf["path"]

        print(f"\n📄 Workflow: {name}")
        print(f"Arquivo: {path}")

        content = get_workflow_file(path)
        analysis = analyze_workflow(content)

        print("Análise:")

        for item, status in analysis.items():
            icon = "✅" if status else "❌"
            print(f" {icon} {item}")

    print("\nAnálise finalizada.")


if __name__ == "__main__":
    main()