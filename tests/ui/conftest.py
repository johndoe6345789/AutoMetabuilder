import os
import time
import multiprocessing
import pytest
import uvicorn
from autometabuilder.web.server import app

def run_server():
    os.environ["MOCK_WEB_UI"] = "true"
    os.environ["WEB_USER"] = "testuser"
    os.environ["WEB_PASSWORD"] = "testpass"
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

@pytest.fixture(scope="session")
def server():
    proc = multiprocessing.Process(target=run_server, daemon=True)
    proc.start()
    # Give the server a moment to start
    time.sleep(2)
    yield "http://127.0.0.1:8001"
    proc.terminate()
