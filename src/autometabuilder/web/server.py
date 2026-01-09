import os
import json
import secrets
from fastapi import FastAPI, Request, Form, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv, set_key
import subprocess
import sys

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

# Setup templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

def run_bot_task():
    global bot_process
    try:
        # Run main.py as a subprocess with --yolo --once
        cmd = [sys.executable, "-m", "autometabuilder.main", "--yolo", "--once"]
        bot_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        bot_process.wait()
    finally:
        bot_process = None

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
        if "=" in line and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            env_vars[key] = value
    return env_vars

def get_translations():
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

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, username: str = Depends(get_current_user)):
    logs = get_recent_logs()
    env_vars = get_env_vars()
    translations = get_translations()
    prompt_content = get_prompt_content()
    is_running = bot_process is not None
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "logs": logs, 
        "env_vars": env_vars,
        "translations": translations,
        "prompt_content": prompt_content,
        "is_running": is_running,
        "username": username
    })

@app.post("/run")
async def run_bot(background_tasks: BackgroundTasks, username: str = Depends(get_current_user)):
    global bot_process
    if bot_process is None:
        background_tasks.add_task(run_bot_task)
    return RedirectResponse(url="/", status_code=303)

@app.post("/prompt")
async def update_prompt(content: str = Form(...), username: str = Depends(get_current_user)):
    prompt_path = os.environ.get("PROMPT_PATH", "prompt.yml")
    with open(prompt_path, "w", encoding="utf-8") as f:
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

@app.get("/api/status")
async def get_status(username: str = Depends(get_current_user)):
    return {"is_running": bot_process is not None}

@app.get("/api/logs")
async def get_logs(username: str = Depends(get_current_user)):
    return {"logs": get_recent_logs()}

@app.post("/translations")
async def create_translation(lang: str = Form(...), username: str = Depends(get_current_user)):
    pkg_dir = os.path.dirname(os.path.dirname(__file__))
    en_path = os.path.join(pkg_dir, "messages_en.json")
    new_path = os.path.join(pkg_dir, f"messages_{lang}.json")
    
    if not os.path.exists(new_path):
        with open(en_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        with open(new_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
            
    return RedirectResponse(url="/", status_code=303)

def start_web_ui(host="0.0.0.0", port=8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
