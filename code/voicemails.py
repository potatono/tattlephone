import os
import time
import threading
import random
from datetime import datetime

import config
from voicemail import Voicemail

class Voicemails:
    def __init__(self):
        self.voicemails = {}
        self.listeners = []
        self.monitoring = False
        self.min_duration = config.tattle_duration

    def read(self):
        # Gross
        self.num = 1
        self.times = {}
        self.read_path(config.tattle_vm_inbox_path)
        self.read_path(config.tattle_vm_old_path)

        for k, v in self.voicemails.items():
            if v.time not in self.times:
                del self.voicemails[v.time]

    def read_path(self, path):
        lst = os.listdir(path)
        numbers = [int(f[3:7]) for f in lst if f.endswith('.txt')]

        for number in numbers:
            v = Voicemail(path, number)
            v.num = self.num
            self.num += 1

            self.times[v.time] = True
            if v.time not in self.voicemails:

                if v.duration >= self.min_duration:
                    print("Adding {} to voicemails..".format(v.time))
                    self.voicemails[v.time] = v
                    self.dispatch(v)
   

    def add_listener(self, listener):
        self.listeners.append(listener)

    def dispatch(self, voicemail):
        for listener in self.listeners:
            listener(voicemail)

    def monitor(self):
        if self.monitoring:
            return

        self.monitoring = True

        def loop():
            while self.monitoring:
                self.read()
                time.sleep(1)

        self.thread = threading.Thread(target=loop)
        self.thread.start()

    def stop(self):
        self.monitoring = False
        self.thread.join()

    def random(self):
        vms = list(self.voicemails.values())

        if len(vms) is 0:
            return None

        return vms[random.randint(0, len(vms) - 1)]

    def shuffled(self):
        vms = list(self.voicemails.values())

        random.shuffle(vms)

        return vms

