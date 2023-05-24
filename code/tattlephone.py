#!/usr/bin/env python3

import pystrix
import os
import sys
import random
import re
import logging
import time
import threading

import config
from voicemails import Voicemails
from voicemail import Voicemail
from call import Call


logger = logging.getLogger()
logger.setLevel("INFO")

formatter = logging.Formatter("%(asctime)s [%(levelname)-5s] %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

handler = logging.FileHandler("/var/log/agi/tattlephone.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

class FastAGIServer(threading.Thread):
    fagi_server = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        logging.info("REGISTER")
        self.fagi_server = pystrix.agi.FastAGIServer()
        self.fagi_server.register_script_handler(None, self.handler)

        self.voicemails = Voicemails()
        self.voicemails.read()


    def kill(self):
        logging.info("KILL")
        self.fagi_server.shutdown()

    def run(self):
        logging.info("RUN")
        self.fagi_server.serve_forever()

    def playback_announce(self):
        self.agi.execute(pystrix.agi.core.StreamFile('custom/OutgoingMessage'))
        self.agi.execute(pystrix.agi.core.StreamFile('you-can-press'))
        self.agi.execute(pystrix.agi.core.SayAlpha('#'))
        self.agi.execute(pystrix.agi.core.StreamFile('to-accept-recording'))
    
#    def get_next_tattle_number(self):
#
#        files = os.listdir(config.tattles_path)
#        maxnum = 0
#    
#        for f in files:
#            n = re.sub('\\D','',f)
#    
#            if not n:
#                continue
#    
#            maxnum = max(int(n), maxnum)
#    
#        return maxnum + 1
    
    def get_tattles(self):
        tattles = self.voicemails.shuffled()

        return tattles[0:config.tattles_to_play]
    
    def record_tattle(self):
        msgnum = self.voicemails.get_next_number()
        vm = Voicemail(msgnum)
        path = vm.audio_path[0:-4]
        t = time.time()
        hangup = False
    
        try:
            logger.info("Recording {}".format(path))
            self.agi.execute(pystrix.agi.core.RecordFile(path, timeout=config.max_tattle_length * 1000, escape_digits='1234567890*#'))
        except pystrix.agi.AGIHangup:
            hangup = True
    
        recording_time = int(time.time() - t)

        logger.info("Tattle is {}s long".format(recording_time))

        vm.write(recording_time)
        self.voicemails.add(vm)
    
        return (recording_time, hangup, msgnum)
    
    def get_tattle_number(self, tattle):
        return int(re.sub("\\D","",tattle))
        
    def callback_with_tattles(self):
        tattles = self.get_tattles()
        call = Call()
        path = call.write(tattles)
        answered = call.execute(path)
    
    def playback_tattles(self):
        tattles = self.get_tattles()
        logging.info(tattles)
        
        for tattle in tattles:
            num = tattle.num
            path = tattle.audio_path
            logging.info("Saying {}".format(num))
            self.agi.execute(pystrix.agi.core.SayAlpha(num))
            logging.info("Playing {}".format(path))
            self.agi.execute(pystrix.agi.core.StreamFile(path[0:-4], escape_digits='1234567890*#'))
        
        logging.info("Playing yes-dear")
        self.agi.execute(pystrix.agi.core.StreamFile('yes-dear'))
        self.agi.execute(pystrix.agi.core.StreamFile('get_bleep_outta'))
    
    def playback_too_short(self):
        self.agi.execute(pystrix.agi.core.StreamFile('your-msg-is-too-short'))
    
    def handler(self, agi, args, kwargs, match, path):
        try:
            self.agi = agi

            logging.info("ANSWER")
            agi.execute(pystrix.agi.core.Answer())
    
            logging.info("IRA")
            self.playback_announce()
    
            logging.info("RECORD")
            (tattle_time, hangup, tattle_num) = self.record_tattle()
    
            if tattle_time >= config.min_tattle_length:
                logging.info("TATTLES")
                if hangup:
                    logging.info("CALLBACK")
                    self.callback_with_tattles()
                    return
                else:
                    logging.info("PLAYBACK")
                    self.playback_tattles()
            else:
                self.playback_too_short()
    
            logging.info("GOODBYE")
            agi.execute(pystrix.agi.core.StreamFile('goodbye'))
            logging.info("HANGUP")
            agi.execute(pystrix.agi.core.Hangup())
        except pystrix.agi.AGIHangup as err:
            logging.info("User hung up")
        except Exception as err:
            logging.error(err)

if __name__ == '__main__':
    logger.info("START")
    fastagi_core = FastAGIServer()
    fastagi_core.start()

    while fastagi_core.is_alive():
        time.sleep(1)

    fastagi_core.kill()


# Next steps
#1. Add proper logging
#2. After a recording of a proper length play some tattles
#3. If hungup call back with either tattles or too short msg
#4. Make it fastagi

