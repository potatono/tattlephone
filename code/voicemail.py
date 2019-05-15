import os
import configparser
import shutil
from datetime import datetime
import pytz
import shutil

import config

class Voicemail:
    def __init__(self, num):
        self.num = num
        self.spool_path = config.tattle_vm_path
        self.meta_path = os.path.join(self.spool_path,
                                      "msg{:04d}.txt".format(num))
        self.audio_path = os.path.join(self.spool_path,
                                      "msg{:04d}.wav".format(num))
        self.drop_path = config.tattle_drop_path

        self.read()

    def read(self):
        config = configparser.ConfigParser()
        config.read(self.meta_path)

        message = config['message']
        time = int(message['origtime'])
        self.time = datetime.fromtimestamp(time, tz=pytz.UTC)
        self.time = self.time.astimezone(pytz.timezone('America/New_York'))
        self.duration = int(message['duration'])

    def prep_playback(self, suffix=None):
        path = self.drop_path

        if suffix is not None:
            parts = os.path.splitext(path)
            path = parts[0] + str(suffix) + parts[1]

        shutil.copy(self.audio_path, path)

