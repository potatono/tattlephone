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
        self.spool_path = config.tattles_path
        self.meta_path = os.path.join(self.spool_path,
                                      "tattle{:04d}.txt".format(num))
        self.audio_path = os.path.join(self.spool_path,
                                      "tattle{:04d}.wav".format(num))
        self.drop_path = config.tattle_drop_path

        self.origtime = int(datetime.utcnow().timestamp())
        self.time = datetime.fromtimestamp(self.origtime, tz=pytz.UTC)
        self.time = self.time.astimezone(pytz.timezone('America/New_York'))
        self.duration = 0
        #self.read()
        

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

    def write(self, duration):
        config = configparser.ConfigParser()

        config['message'] = {
                'origtime': self.origtime,
                'duration': duration
        }
        with open(self.meta_path, 'w') as configfile:
            config.write(configfile)

    def prep_playback(self):
        path = self.drop_path

        #parts = os.path.splitext(path)
        #path = parts[0] + str(self.num) + parts[1]

        shutil.copy(self.audio_path, path)

