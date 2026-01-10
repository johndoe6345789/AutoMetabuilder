import subprocess
import os
import logging

logger = logging.getLogger("autometabuilder.docker")

def run_command_in_docker(image: str, command: str, volumes: dict = None, workdir: str = None):
    """
    Run a command inside a Docker container.
    
    :param image: Docker image to use.
    :param command: Command to execute.
    :param volumes: Dictionary of volume mappings {host_path: container_path}.
    :param workdir: Working directory inside the container.
    :return: Standard output of the command.
    """
    docker_command = ["docker", "run", "--rm"]
    
    if volumes:
        for host_path, container_path in volumes.items():
            docker_command.extend(["-v", f"{os.path.abspath(host_path)}:{container_path}"])
            
    if workdir:
        docker_command.extend(["-w", workdir])
        
    docker_command.append(image)
    docker_command.extend(["sh", "-c", command])
    
    logger.info(f"Executing in Docker ({image}): {command}")
    result = subprocess.run(docker_command, capture_output=True, text=True, check=False)
    
    output = result.stdout
    if result.stderr:
        output += "\n" + result.stderr
        
    logger.info(output)
    return output
