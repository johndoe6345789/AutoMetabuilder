import os
import json
import secrets
from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv, set_key
import subprocess
import sys
from ..roadmap_utils import is_mvp_reached

app = FastAPI()
security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.environ.get("WEB_USER")
    correct_password = os.environ.get("WEB_PASSWORD")
    
    # If no credentials are set in env, allow access (for backward compatibility/easier setup)
    if not correct_username or not correct_password:
        return credentials.username

    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Global variable to track if a bot is running
bot_process = None
mock_running = False
current_run_config = {}

# Setup templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Custom Jinja2 filters for prompt parsing
def extract_system_content(yaml_content):
    """Extract system message content from prompt.yml"""
    import re
    match = re.search(r'role:\s*system\s+content:\s*>-?\s*([\s\S]*?)(?=\s*-\s*role:|$)', yaml_content)
    if match:
        content = match.group(1).strip()
        # Remove indentation
        lines = content.split('\n')
        return '\n'.join(line.strip() for line in lines if line.strip())
    return ""

def extract_user_content(yaml_content):
    """Extract user message content from prompt.yml"""
    import re
    match = re.search(r'role:\s*user\s+content:\s*>-?\s*([\s\S]*?)(?=\s*model:|$)', yaml_content)
    if match:
        content = match.group(1).strip()
        # Remove indentation
        lines = content.split('\n')
        return '\n'.join(line.strip() for line in lines if line.strip())
    return ""

templates.env.filters['extract_system_content'] = extract_system_content
templates.env.filters['extract_user_content'] = extract_user_content

def build_prompt_yaml(system_content, user_content, model):
    def indent_block(text):
        lines = (text or "").splitlines()
        if not lines:
            return ""
        return "\n      ".join(line.rstrip() for line in lines)

    model_value = model or "openai/gpt-4o"
    system_block = indent_block(system_content)
    user_block = indent_block(user_content)
    return f"""messages:
  - role: system
    content: >-
      {system_block}
  - role: user
    content: >-
      {user_block}
model: {model_value}
"""

# Setup static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

def run_bot_task(mode="once", iterations=1, yolo=True, stop_at_mvp=False):
    global bot_process, mock_running, current_run_config
    current_run_config = {"mode": mode, "iterations": iterations, "yolo": yolo, "stop_at_mvp": stop_at_mvp}

    if os.environ.get("MOCK_WEB_UI") == "true":
        mock_running = True
        import time
        time.sleep(5)
        mock_running = False
        current_run_config = {}
        return

    try:
        cmd = [sys.executable, "-m", "autometabuilder.main"]

        if yolo:
            cmd.append("--yolo")

        if mode == "once":
            cmd.append("--once")
        # For "yolo" mode (continuous), don't add --once
        # For "iterations" mode, we run multiple times

        if mode == "iterations" and iterations > 1:
            for i in range(iterations):
                if stop_at_mvp and is_mvp_reached():
                    break
                bot_process = subprocess.Popen(cmd + ["--once"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                bot_process.wait()
        else:
            bot_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            bot_process.wait()
    finally:
        bot_process = None
        current_run_config = {}

def get_recent_logs(n=50):
    log_file = "autometabuilder.log"
    if not os.path.exists(log_file):
        return "No logs found."
    with open(log_file, "r") as f:
        lines = f.readlines()
        return "".join(lines[-n:])

def get_env_vars():
    env_path = ".env"
    if not os.path.exists(env_path):
        return {}
    with open(env_path, "r") as f:
        lines = f.readlines()
    
    env_vars = {}
    for line in lines:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            # Remove quotes if present
            if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            env_vars[key] = value
    return env_vars

def get_metadata():
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata_path = os.path.join(pkg_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        return {}
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_ui_assets():
    assets_path = os.path.join(os.path.dirname(__file__), "ui_assets.json")
    if not os.path.exists(assets_path):
        return {"core_scripts": [], "workflow_scripts": [], "page_scripts": []}
    try:
        with open(assets_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return {"core_scripts": [], "workflow_scripts": [], "page_scripts": []}
    if not isinstance(data, dict):
        return {"core_scripts": [], "workflow_scripts": [], "page_scripts": []}
    return data

def load_translation_file(messages_map, lang):
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    messages_file = messages_map.get(lang, f"messages_{lang}.json")
    messages_path = os.path.join(pkg_dir, messages_file)
    if not os.path.exists(messages_path):
        return {}
    try:
        with open(messages_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def get_ui_messages():
    metadata = get_metadata()
    messages_map = metadata.get("messages", {})
    lang = os.environ.get("APP_LANG", "en")
    base_messages = load_translation_file(messages_map, "en")
    localized_messages = load_translation_file(messages_map, lang)
    merged = dict(base_messages)
    merged.update(localized_messages)
    return merged, lang

def get_translations():
    metadata = get_metadata()
    messages_map = metadata.get("messages", {})
    if messages_map:
        return messages_map
    
    # Fallback to scanning if metadata is empty
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    files = [f for f in os.listdir(pkg_dir) if f.startswith("messages_") and f.endswith(".json")]
    translations = {}
    for f in files:
        lang = f[len("messages_"):-len(".json")]
        translations[lang] = f
    return translations

def get_prompt_content():
    prompt_path = os.environ.get("PROMPT_PATH", "prompt.yml")
    if not os.path.exists(prompt_path):
        return ""
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def get_workflow_content():
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    workflow_file = metadata.get("workflow_path", "workflow.json")
    workflow_path = os.path.join(pkg_dir, workflow_file)
    if not os.path.exists(workflow_path):
        return ""
    with open(workflow_path, "r", encoding="utf-8") as f:
        return f.read()

def get_workflow_packages_dir():
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    packages_dir = metadata.get("workflow_packages_path", "workflow_packages")
    return os.path.join(pkg_dir, packages_dir)

def load_workflow_packages():
    packages_dir = get_workflow_packages_dir()
    if not os.path.isdir(packages_dir):
        return []
    packages = []
    for filename in sorted(os.listdir(packages_dir)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(packages_dir, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict):
            continue
        package_id = data.get("id") or os.path.splitext(filename)[0]
        data["id"] = package_id
        if "workflow" not in data:
            data["workflow"] = {"nodes": []}
        packages.append(data)
    return packages

def get_navigation_items():
    return [
        {
            "section": "dashboard",
            "icon": "speedometer2",
            "label_key": "ui.nav.dashboard",
            "default_label": "Dashboard"
        },
        {
            "section": "workflow",
            "icon": "diagram-3",
            "label_key": "ui.nav.workflow",
            "default_label": "Workflow"
        },
        {
            "section": "prompt",
            "icon": "file-text",
            "label_key": "ui.nav.prompt",
            "default_label": "Prompt"
        },
        {
            "section": "settings",
            "icon": "gear",
            "label_key": "ui.nav.settings",
            "default_label": "Settings"
        },
        {
            "section": "translations",
            "icon": "translate",
            "label_key": "ui.nav.translations",
            "default_label": "Translations"
        }
    ]

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, username: str = Depends(get_current_user)):
    logs = get_recent_logs()
    env_vars = get_env_vars()
    translations = get_translations()
    metadata = get_metadata()
    ui_assets = get_ui_assets()
    prompt_content = get_prompt_content()
    workflow_content = get_workflow_content()
    is_running = bot_process is not None or mock_running
    mvp_status = is_mvp_reached()
    ui_messages, ui_lang = get_ui_messages()

    def t(key, default=""):
        return ui_messages.get(key, default or key)

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "logs": logs, 
        "env_vars": env_vars,
        "translations": translations,
        "metadata": metadata,
        "ui_assets": ui_assets,
        "prompt_content": prompt_content,
        "workflow_content": workflow_content,
        "is_running": is_running,
        "mvp_reached": mvp_status,
        "username": username,
        "ui_messages": ui_messages,
        "ui_lang": ui_lang,
        "t": t
    })

@app.post("/run")
async def run_bot(
    background_tasks: BackgroundTasks,
    mode: str = Form("once"),
    iterations: int = Form(1),
    yolo: bool = Form(True),
    stop_at_mvp: bool = Form(False),
    username: str = Depends(get_current_user)
):
    global bot_process, mock_running
    if bot_process is None and not mock_running:
        background_tasks.add_task(run_bot_task, mode, iterations, yolo, stop_at_mvp)
    return RedirectResponse(url="/", status_code=303)

@app.post("/prompt")
async def update_prompt(
    content: str = Form(""),
    system_content: str = Form(""),
    user_content: str = Form(""),
    model: str = Form("openai/gpt-4o"),
    prompt_mode: str = Form("builder"),
    username: str = Depends(get_current_user)
):
    prompt_path = os.environ.get("PROMPT_PATH", "prompt.yml")
    if prompt_mode == "raw":
        prompt_yaml = content
    else:
        prompt_yaml = build_prompt_yaml(system_content, user_content, model)
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt_yaml)
    return RedirectResponse(url="/", status_code=303)

@app.post("/workflow")
async def update_workflow(content: str = Form(...), username: str = Depends(get_current_user)):
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    workflow_file = metadata.get("workflow_path", "workflow.json")
    workflow_path = os.path.join(pkg_dir, workflow_file)
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(content)
    return RedirectResponse(url="/", status_code=303)

@app.post("/settings")
async def update_settings(request: Request, username: str = Depends(get_current_user)):
    form_data = await request.form()
    env_path = ".env"
    for key, value in form_data.items():
        if key.startswith("env_"):
            env_key = key[4:]
            set_key(env_path, env_key, value)
    
    # Handle new setting
    new_key = form_data.get("new_env_key")
    new_value = form_data.get("new_env_value")
    if new_key and new_value:
        set_key(env_path, new_key, new_value)
        
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/ui-context", response_class=JSONResponse)
async def get_ui_context(username: str = Depends(get_current_user)):
    ui_messages, ui_lang = get_ui_messages()
    return {"lang": ui_lang, "messages": ui_messages}

@app.get("/api/status")
async def get_status(username: str = Depends(get_current_user)):
    return {
        "is_running": bot_process is not None or mock_running,
        "mvp_reached": is_mvp_reached()
    }

@app.get("/api/workflow/plugins", response_class=JSONResponse)
async def get_workflow_plugins():
    metadata = get_metadata()
    return metadata.get("workflow_plugins", {})

@app.get("/api/workflow/packages", response_class=JSONResponse)
async def list_workflow_packages():
    packages = load_workflow_packages()
    summarized = []
    for package in packages:
        summarized.append({
            "id": package.get("id"),
            "label": package.get("label", ""),
            "description": package.get("description", ""),
            "tags": package.get("tags", [])
        })
    return {"packages": summarized}

@app.get("/api/workflow/packages/{package_id}", response_class=JSONResponse)
async def get_workflow_package(package_id: str):
    packages = load_workflow_packages()
    for package in packages:
        if package.get("id") == package_id:
            return package
    raise HTTPException(status_code=404, detail="Workflow package not found")

@app.get("/api/navigation", response_class=JSONResponse)
async def get_navigation():
    return {"items": get_navigation_items()}

@app.get("/api/logs")
async def get_logs(username: str = Depends(get_current_user)):
    return {"logs": get_recent_logs()}

@app.post("/translations")
async def create_translation(lang: str = Form(...), username: str = Depends(get_current_user)):
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    messages_map = metadata.get("messages", {})

    en_file = messages_map.get("en", "messages_en.json")
    en_path = os.path.join(pkg_dir, en_file)

    new_file = f"messages_{lang}.json"
    new_path = os.path.join(pkg_dir, new_file)

    if not os.path.exists(new_path):
        with open(en_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        with open(new_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)

        # Update metadata.json
        messages_map[lang] = new_file
        metadata["messages"] = messages_map
        metadata_path = os.path.join(pkg_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

    return RedirectResponse(url="/#translations", status_code=303)

@app.get("/api/translations/{lang}")
async def get_translation(lang: str, username: str = Depends(get_current_user)):
    """Get translation content for a specific language"""
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    messages_map = metadata.get("messages", {})

    if lang not in messages_map:
        raise HTTPException(status_code=404, detail=f"Translation '{lang}' not found")

    file_path = os.path.join(pkg_dir, messages_map[lang])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Translation file not found")

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    return {"lang": lang, "file": messages_map[lang], "content": content}

@app.put("/api/translations/{lang}")
async def update_translation(lang: str, request: Request, username: str = Depends(get_current_user)):
    """Update translation content for a specific language"""
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    messages_map = metadata.get("messages", {})

    if lang not in messages_map:
        raise HTTPException(status_code=404, detail=f"Translation '{lang}' not found")

    file_path = os.path.join(pkg_dir, messages_map[lang])
    data = await request.json()

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data.get("content", {}), f, indent=2, ensure_ascii=False)

    return {"success": True, "lang": lang}

@app.delete("/api/translations/{lang}")
async def delete_translation(lang: str, username: str = Depends(get_current_user)):
    """Delete a translation (cannot delete 'en')"""
    if lang == "en":
        raise HTTPException(status_code=400, detail="Cannot delete the default English translation")

    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    metadata = get_metadata()
    messages_map = metadata.get("messages", {})

    if lang not in messages_map:
        raise HTTPException(status_code=404, detail=f"Translation '{lang}' not found")

    file_path = os.path.join(pkg_dir, messages_map[lang])

    # Delete the file
    if os.path.exists(file_path):
        os.remove(file_path)

    # Update metadata
    del messages_map[lang]
    metadata["messages"] = messages_map
    metadata_path = os.path.join(pkg_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return {"success": True, "lang": lang}

def start_web_ui(host="0.0.0.0", port=8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
