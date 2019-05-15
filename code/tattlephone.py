import os
from datetime import datetime
import time

import config
from voicemails import Voicemails
from call import Call
import pytz

class Tattlephone:
    def __init__(self):
        self.voicemails = Voicemails()
        self.voicemails.read()
        self.voicemails.add_listener(self.register_activity)
        self.voicemails.monitor()
        self.register_activity()

    def now(self):
        tz = pytz.timezone('America/New_York')
        dt = pytz.utc.localize(datetime.now()).astimezone(tz)

        return dt

    def is_calling_hour(self):
        dt = self.now()

        for hours in config.calling_hours:
            if dt.hour >= hours[0] and dt.hour <=hours[1]:
                return True

        return False

    def is_idle(self):
        dt = self.now() - self.last_activity

        return dt.seconds >= config.calling_idle_time

    def start(self):
        while True:
            time.sleep(10)
            print("Is calling hour?", self.is_calling_hour())
            print("Is idle?", self.is_idle())
            if self.is_calling_hour() and self.is_idle():
                self.call()

    def call(self):
        print("Calling!")
        vms = self.voicemails
        vms.filter()
        vms = vms.shuffled()
        num = min(len(vms), 1)
        for i in range(num):
            vms[i].prep_playback(i)

        print("Playing %d tattles.." % num)
        call = Call()
        path = call.write(num)
        call.execute(path)
        print(path)

    def register_activity(self, activity=None):
        self.last_activity = self.now()
        print("Activity at {}".format(self.last_activity))

if __name__ == "__main__":
    tattlephone = Tattlephone()
    tattlephone.start()
        
