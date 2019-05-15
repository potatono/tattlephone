import os
import time
import threading
import random

import config
from voicemail import Voicemail

class Voicemails:
    def __init__(self):
        self.spool_path = config.tattle_vm_path
        self.voicemails = {}
        self.listeners = []
        self.monitoring = False

    def read(self):
        lst = os.listdir(self.spool_path)
        numbers = [int(f[3:7]) for f in lst if f.endswith('.txt')]

        for number in numbers:
            if number not in self.voicemails:
                v = Voicemail(number)
                self.voicemails[number] = v
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

    def filter(self, duration=15):
        self.voicemails = { k: v for k, v in self.voicemails.items() 
                if v.duration > duration }

    def random(self):
        vms = list(self.voicemails.values())

        if len(vms) is 0:
            return None

        return vms[random.randint(0, len(vms) - 1)]

    def shuffled(self):
        vms = list(self.voicemails.values())

        random.shuffle(vms)

        return vms

