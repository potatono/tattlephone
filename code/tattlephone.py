import os
from datetime import datetime
from datetime import timedelta
import time

import config
from voicemails import Voicemails
from call import Call
import pytz

class Tattlephone:
    def __init__(self):
        self.voicemails = Voicemails()
        self.voicemails.read()
        self.voicemails.add_listener(self.on_voicemail)
        self.voicemails.monitor()
        self.call_in(minutes=0, afterhours=True)

    def now(self):
        tz = pytz.timezone(config.tz)
        dt = pytz.utc.localize(datetime.now()).astimezone(tz)

        return dt

    def is_calling_hour(self):
        dt = self.now()

        for hours in config.calling_hours:
            if dt.hour >= hours[0] and dt.hour <=hours[1]:
                return True

        return False

    def on_voicemail(self, voicemail):
        if voicemail.duration >= config.tattle_duration:
            self.call_in(config.call_mins_after_tattle, afterhours=True)
        else:
            print("Voicemail too short {}<{}:".format(voicemail.duration, config.tattle_duration))

    def start(self):
        while True:
            print("Now:      ", self.now())
            print("Next call:", self.next_call)
            print("Next call after hours?", self.next_call_afterhours)
            print("Is calling hour?", self.is_calling_hour())

            if self.now() >= self.next_call:
                if self.is_calling_hour() or self.next_call_afterhours:
                    print("Calling!")
                    self.next_call_afterhours = False
                    self.call()
                else:
                    print("Cannot call after hours.")

            if self.has_play_request():
                print("Calling for play request!")
                self.call()

            time.sleep(3)

    def call(self):
        vms = self.voicemails
        vms = vms.shuffled()
        num = 10

        print("Playing %d tattles.." % num)
        call = Call()
        path = call.write(vms[0:num])
        answered = call.execute(path)

        if answered:
            self.call_in(config.call_mins_after_answer)
        else:
            self.call_in(config.call_mins_after_no_answer)

    def call_in(self, minutes, afterhours=False):
        self.next_call = self.now() + timedelta(minutes=minutes)
        self.next_call_afterhours = afterhours
        print("Calling again in {} minutes at {}, afterhours={}".format(minutes, self.next_call, afterhours))

    def has_play_request(self):
        if os.path.exists(config.tattle_play_request):
            os.remove(config.tattle_play_request)
            time.sleep(5)

            return True

        return False

if __name__ == "__main__":
    tattlephone = Tattlephone()
    tattlephone.start()
        
