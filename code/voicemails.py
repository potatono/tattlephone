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
        self.maxnum = 0
        self.times = {}
        self.read_path(config.tattle_vm_inbox_path)
        #self.read_path(config.tattle_vm_old_path)

        for k, v in self.voicemails.items():
            if v.time not in self.times:
                del self.voicemails[v.time]

    def read_path(self, path):
        lst = os.listdir(path)
        start = len('tattle')
        numbers = [int(f[start:start+4]) for f in lst if f.endswith('.txt')]

        for number in numbers:
            v = Voicemail(number)
            v.read()
            v.num = number
            self.maxnum = max(self.maxnum, number)

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

    def get_next_number(self):
        return self.maxnum + 1


    def add(self, vm):
        self.voicemails[vm.time] = vm
        self.maxnum = max(self.maxnum, vm.num)

