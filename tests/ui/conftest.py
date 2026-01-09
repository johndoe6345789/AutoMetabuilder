import os
import time
import socket
import threading
import pytest
import uvicorn
from autometabuilder.web.server import app

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "chromium_sandbox": False,
        "args": ["--disable-setuid-sandbox"],
    }

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "http_credentials": {
            "username": "testuser",
            "password": "testpass"
        }
    }

def run_server(port, holder):
    os.environ["MOCK_WEB_UI"] = "true"
    os.environ["WEB_USER"] = "testuser"
    os.environ["WEB_PASSWORD"] = "testpass"
    os.environ["APP_LANG"] = "en"
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    holder["server"] = server
    server.run()

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

@pytest.fixture(scope="session")
def server():
    port = get_free_port()
    holder = {}
    thread = threading.Thread(target=run_server, args=(port, holder), daemon=True)
    thread.start()
    # Give the server a moment to start
    time.sleep(2)
    yield f"http://127.0.0.1:{port}"
    server = holder.get("server")
    if server:
        server.should_exit = True
    thread.join(timeout=3)
