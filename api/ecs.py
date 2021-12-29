import os
import requests
from urllib.parse import urljoin
from starlette.datastructures import URL
from typing import Final


def get_task_metadata(base_url: URL):
    print(type(base_url))
    ecs_container_metadata_url = os.getenv('ECS_CONTAINER_METADATA_URI_V4')
    BACKUP_URI: Final[str] = urljoin(str(base_url), 'static/missing_env.json')
    ECS_TASK_URI: Final[str] = urljoin(ecs_container_metadata_url, 'task')

    request_url = BACKUP_URI if ecs_container_metadata_url is None else ECS_TASK_URI

    response = requests.get(request_url)
    response.raise_for_status()
    return response.json()
