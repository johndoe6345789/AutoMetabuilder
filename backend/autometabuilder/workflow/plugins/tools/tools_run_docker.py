"""Workflow plugin: run command in Docker container."""
from ....docker_utils import run_command_in_docker


def run(_runtime, inputs):
    """
    Run a command inside a Docker container.
    
    Inputs:
    - image: Docker image to use
    - command: Command to execute
    - volumes: Optional dict of volume mappings {host_path: container_path}
    - workdir: Optional working directory inside the container
    """
    image = inputs.get("image")
    command = inputs.get("command")
    volumes = inputs.get("volumes")
    workdir = inputs.get("workdir")
    
    if not image or not command:
        return {"error": "Both 'image' and 'command' are required"}
    
    output = run_command_in_docker(image, command, volumes, workdir)
    return {"output": output}
