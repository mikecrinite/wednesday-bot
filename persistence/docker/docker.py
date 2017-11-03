import docker
import logging

# Set up logging
docker_logger = logging.getLogger('wednesday.docker')
docker_logger.setLevel(logging.INFO)

# Setup Docker, and start mysql container
client = docker.from_env()
client.containers.run("mysql/mysql", detach=True)

# Point a reference at the mysql container
all_containers = client.containers.list()
mysql_id = None

if len(all_containers) == 1:
    mysql_id = all_containers[1].id
else:
    raise ValueError("Unexpected number of running containers")

if mysql_id is not None:
    mysql = client.containers.get(mysql_id)
else:
    raise EnvironmentError("Couldn't find mysql container")

# Do things
mysql.exec_run('echo lmaoooooooooo')

def stream_logs():
    """
    Stream logs from mysql container
    """
    for line in mysql.logs(stream=True):
        docker_logger.info(line.strip())
