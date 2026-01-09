import os
import requests
import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

RAW_PROMPT_URL = "https://raw.githubusercontent.com/johndoe6345789/metabuilder/main/getonwithit.prompt.yml"

def load_prompt_yaml(url: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return yaml.safe_load(r.text)

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return

    endpoint = "https://models.github.ai/inference"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    prompt = load_prompt_yaml(RAW_PROMPT_URL, token)

    messages = prompt["messages"]
    model = prompt.get("model", "openai/gpt-4.1")

    # Add runtime request (optional)
    messages = messages + [{"role": "user", "content": "What should I do next?"}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1.0,
        top_p=1.0,
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
