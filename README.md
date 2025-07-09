<h1>docker-monitoring</h1> 


This is a simple Python project for monitoring a Docker container. It sends an email notification with the container's 
logs if it stops running.

## How it works
The script takes a container ID as an argument and periodically checks if the container is still running. If it detects 
that the container has stopped, it will:
1.  Capture the logs from the stopped container.
2.  Email a list of specified recipients. The email will contain the container ID, the time it stopped, and 
the captured logs.

## Configuration
The application requires an `email_config.ini` file to handle email notifications. This file must be in JSON format and 
contain the necessary credentials for the email account that will send the notifications, as well as the list of 
recipients.

The `email_config.ini` file should look like this:

```json
{
    "bot_email": "your_sender_email@gmail.com",
    "bot_pwd": "your_gmail_app_password",
    "list_rec": ["recipient1@example.com", "recipient2@example.com"]
}
```

### Fields
*   `bot_email`: The Gmail address that will be used to send the notification emails.
*   `bot_pwd`: The **App Password** for the sender's Gmail account. For security reasons, it is now necessary to 
use an App Password instead of your regular account password. You can generate one from your Google Account settings.
*   `list_rec`: A list of email addresses that will receive the notification.

## Prerequisites
*   Python 3.12
*   Docker
*   [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation
Clone the repository and install uv if you haven't already. Initiate the environment with the following command:
```bash
cd docker-monitoring
uv sync
```
Install the current package:
```bash
uv pip install -e .
```

## Usage
You can run the monitor from the command line. You must provide the ID of the container you wish to monitor.
Activate the virtual environment if you haven't already:
```bash
uv venv
source .venv/bin/activate # On Windows, use .venv\Scripts\activate
```
Then, run the following command, replacing `<CONTAINER_ID>` with the actual ID of the Docker container you want to 
monitor:

```bash
python -m src.docker-monitoring -i <CONTAINER_ID> -c <PATH_TO_EMAIL_CONFIG> -r <REFRESH_RATE>
```

### Command-Line Arguments
*   `-i` or `--id` (required): The ID (long or short) of the container to monitor.
*   `-c` or `--config` (optional): The path to your email configuration file. Defaults to `email_config.ini`.
*   `-r` or `--refresh` (optional): The refresh rate in seconds for checking the container's status. Defaults to `60`.

### Example
To monitor a container with the ID `5486aea24593`, check its status every 5 seconds, and use a config file located at `conf/my_config.ini`:
```bash
python -m src.docker-monitoring --id 5486aea24593 --refresh 5 --config conf/my_config.ini
```