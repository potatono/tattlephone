import os
import configparser
import shutil
from datetime import datetime
import pytz
import shutil

import config

class Voicemail:
    def __init__(self, spool_path, num):
        self.num = num
        self.spool_path = spool_path
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
        self.origtime = message['origtime']
        self.time = datetime.fromtimestamp(time, tz=pytz.UTC)
        self.time = self.time.astimezone(pytz.timezone('America/New_York'))
        self.duration = int(message['duration'])
        
        parts = os.path.splitext(self.drop_path)
        self.drop_path = parts[0] + message['origtime'] + parts[1]
        self.sound_name = 'custom/tattle' + message['origtime']

    def prep_playback(self):
        path = self.drop_path

        #parts = os.path.splitext(path)
        #path = parts[0] + str(self.num) + parts[1]

        shutil.copy(self.audio_path, path)

