import datetime
import docker
import time
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class ContainerObserver:
    def __init__(self, container_id: str, config_location: str = 'email_config.ini', refresh_rate: int = 60):
        self.container_id = container_id
        self.container = None
        self.list_emails = None
        self.bot_email = None
        self.bot_pwd = None
        self.refresh_rate = refresh_rate
        self.set_up_emails(config_location)
        self.client = docker.from_env()
        try:
            self.container = self.client.containers.get(self.container_id)
        except docker.errors.NotFound:
            time.sleep(2)
            self.container = self.client.containers.get(self.container_id)


    def is_container_in_list(self) -> bool:
        """
        Checks if there is a container with the given id is in containers.list().
        :return: True if the container is running, False otherwise.
        """
        list_container_id = list(map(lambda cont: cont.id, self.client.containers.list()))
        listener_container_short_id = list(map(lambda cont: cont.short_id, self.client.containers.list()))
        return (self.container_id in list_container_id) or (self.container_id in listener_container_short_id)


    def is_container_running(self) -> bool:
        """
        Checks the status of the container.
        :return:
        """
        return self.container.status == "running"


    def set_up_emails(self, config_file: str):
        """
        read the config file and set up the email variables.
        :param config_file:
        :return:
        """
        with open(config_file, 'r') as f:
            config = json.load(f)
            self.list_emails = config['list_rec']
            self.bot_email = config['bot_email']
            self.bot_pwd = config['bot_pwd']
        assert isinstance(self.list_emails, list)
        assert isinstance(self.bot_email, str)
        assert isinstance(self.bot_pwd, str)


    def notify_accounts(self, msg: str):
        """
        Sends an email to the list of accounts.
        :param msg:
        :return:
        """
        message = MIMEMultipart()
        message["From"] = 'MEDICS Bot'
        message['Subject'] = 'Notification!'
        message.attach(MIMEText(msg, 'plain'))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.bot_email, self.bot_pwd)
            for email in self.list_emails:
                message["To"] = email
                server.send_message(msg=message, from_addr=self.bot_email, to_addrs=email)

    def observe_container(self):
        """
        Continuously observes the status of a container and performs actions when it
        stops running. The method repeatedly checks if the container is running at
        regular intervals, specified by the `refresh_rate`. If the container has
        stopped running, it collects logs, prepares a notification message, and
        sends the message through `notify_accounts`.
        :return: None
        """
        while True:
            if not self.is_container_in_list():
                break
            time.sleep(self.refresh_rate)
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        msg = f"Container {self.container_id} has stopped running as of {current_time} !!!\n"
        # Copy the logs into the message
        msg += 15*"-" + '\n'
        msg += "The following logs were captured\n"
        msg += 15*"-" + '\n\n'
        msg += self.container.logs().decode('utf-8')
        self.notify_accounts(msg)

if __name__ == '__main__':
    obs = ContainerObserver('5486aea24593', refresh_rate=5)
    obs.observe_container()
