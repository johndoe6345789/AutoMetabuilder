import os
import requests
import yaml
from openai import OpenAI

RAW_PROMPT_URL = "https://raw.githubusercontent.com/johndoe6345789/metabuilder/main/getonwithit.prompt.yml"

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.github.ai/inference"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def load_prompt_yaml(url: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    return yaml.safe_load(r.text)

prompt = load_prompt_yaml(RAW_PROMPT_URL)

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
