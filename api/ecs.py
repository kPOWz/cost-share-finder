import os
import requests
from urllib.parse import urljoin
from starlette.datastructures import URL
from typing import Final


def get_task_metadata():
    ecs_container_metadata_url = os.getenv('ECS_CONTAINER_METADATA_URI_V4', None)
    if ecs_container_metadata_url is None:
        return {'missingEnv': 'ECS_CONTAINER_METADATA_URI_V4'}
    response = requests.get(urljoin(ecs_container_metadata_url, 'task'))
    response.raise_for_status()
    return response.json()
