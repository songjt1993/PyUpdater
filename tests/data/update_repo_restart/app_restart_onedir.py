from __future__ import print_function
import os
import sys

from pyupdater.client import Client
from dsdev_utils.paths import get_mac_dot_app_dir

import client_config

APPNAME = 'Acme'
VERSION = '4.1'


def cb(status):
    out = ''
    percent = status.get('percent_complete')
    time = status.get('time')
    if percent is not None:
        out += '{}%'.format(percent)
    if time is not None:
        out += ' - {}'.format(time)
    if len(out) == 0:
        out = 'Nothing yet...'
    sys.stdout.write('\r{}'.format(out))
    sys.stdout.flush()


def main():
    print(VERSION)
    data_dir = None
    config = client_config.ClientConfig()
    if getattr(config, 'USE_CUSTOM_DIR', False):
        print("Using custom directory")
        if (sys.platform == 'darwin' and os.path.dirname(sys.executable
                                                         ).endswith('MacOS')):
            data_dir = os.path.join(get_mac_dot_app_dir(os.path.dirname(
                sys.executable)), '.update')
        else:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(
                sys.executable)), '.update')
    client = Client(config, refresh=True,
                    progress_hooks=[cb], data_dir=data_dir)
    update = client.update_check(APPNAME, VERSION)
    if update is not None:
        print("We have an update")
        retry_count = 0
        while retry_count < 5:
            success = update.download()
            if success is True:
                break
            print("Retry Download. Count {}".format(retry_count + 1))
            retry_count += 1

        if success:
            print('Update download successful')
            print('Restarting')
            update.extract_restart()
        else:
            print('Failed to download update')

    print("Leaving main()")


if __name__ == '__main__':
    main()
