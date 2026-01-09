import os
import time
import socket
import multiprocessing
import pytest
import uvicorn
from autometabuilder.web.server import app

multiprocessing.set_start_method("spawn", force=True)

@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "chromium_sandbox": False,
        "args": ["--disable-setuid-sandbox"],
    }

def run_server(port):
    os.environ["MOCK_WEB_UI"] = "true"
    os.environ["WEB_USER"] = "testuser"
    os.environ["WEB_PASSWORD"] = "testpass"
    os.environ["APP_LANG"] = "en"
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="error")

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

@pytest.fixture(scope="session")
def server():
    port = get_free_port()
    proc = multiprocessing.Process(target=run_server, args=(port,), daemon=True)
    proc.start()
    # Give the server a moment to start
    time.sleep(2)
    yield f"http://127.0.0.1:{port}"
    proc.terminate()
