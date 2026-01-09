"""Run a task inside Docker."""
import os
from ..docker_utils import run_command_in_docker


def run_docker_task(image: str, command: str, workdir: str = "/workspace") -> str:
    """Run a command inside Docker."""
    volumes = {os.getcwd(): "/workspace"}
    return run_command_in_docker(image, command, volumes=volumes, workdir=workdir)
