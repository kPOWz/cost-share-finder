# For more information, please refer to https://aka.ms/vscode-docker-python
# currently 3.10.1
FROM python:slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
# each running process writes its event stream, unbuffered, to stdout
# log destinations are not visible to or configurable by the app, and instead are completely managed by the execution environment
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY . /code


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
