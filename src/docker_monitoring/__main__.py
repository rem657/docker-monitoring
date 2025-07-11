import argparse
from .container_observer import ContainerObserver
import sys

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--id', help='The id of the container to monitor.', type=str, required=True)
    argparser.add_argument('-c', '--config', help='The path to the config file.', default='email_config.ini', type=str)
    argparser.add_argument('-r', '--refresh', help='The refresh rate of the container monitor in seconds.', default=60,
                           type=int)
    args = argparser.parse_args()
    obs = ContainerObserver(container_id=args.id, config_location=args.config, refresh_rate=args.refresh)
    obs.observe_container()

if __name__ == '__main__':
    sys.exit(main())