import os
import sys
import config
import tempfile
import shutil
import stat
import uuid
import time

class Call:
    def __init__(self):
        self.recording = config.tattle_drop_name
        self.waittime = config.phone_ring_wait_time
        self.extension = config.phone_channel
        self.call_exec_prefix = config.call_spool_prefix
        self.call_done_prefix = config.call_spool_outgoing_prefix

    def data_string(self, vms):
        s = "&".join([ self.vm_string(vm) for vm in vms ])
        s += "&yes-dear&get_bleep_outta&beep&beep&beep&beep&beep&silence/10&silence/10&silence/10"

        return s

    def vm_string(self, vm):
        result = self.digits_string(vm.num) + "&custom/tattle{}".format(vm.num)

        print("VM #{} = {}".format(vm.num, result))

        return result

    def digits_string(self, num):
        parts = []

        if num >= 1000:
            thousands = int(num / 1000)
            num = num % 1000
            parts.append("digits/{}".format(thousands))
            parts.append("digits/thousand")

        if num >= 100:
            hundreds = int(num / 100)
            num = num % 100
            parts.append("digits/{}".format(hundreds))
            parts.append("digits/hundred")

        if num >= 20:
            tens = int(num / 10)
            num = num % 10
            parts.append("digits/{}".format(tens * 10))
        
        parts.append("digits/{}".format(num))

        return '&'.join(parts)

    def write(self, vms):
        tmphandle, tmppath = tempfile.mkstemp(text=True, suffix='.call')

        for vm in vms:
            vm.prep_playback()
            
        with os.fdopen(tmphandle, "w") as tmpfile:
            for fh in (tmpfile, sys.stdout):
                print("Channel: {}".format(self.extension), file=fh)
                print("CallerID: \"TATTLEPHONE\" <2>", file=fh)
                print("Application: playback", file=fh)
                print("Data: {}".format(self.data_string(vms)), file=fh)
                print("WaitTime: {}".format(self.waittime), file=fh)
                print("Archive: yes", file=fh)
        
        os.chmod(tmppath, stat.S_IROTH)
        return tmppath

    def execute(self, callpath):
        suffix = uuid.uuid1().hex + '.call'
        shutil.move(callpath, self.call_exec_prefix + suffix)
        time.sleep(self.waittime)

        print(self.call_done_prefix + suffix)
        if os.path.exists(self.call_done_prefix + suffix):
            print("Call not answered")
            answered = False
        else:
            print("Call answered")
            answered = True

        while not os.path.exists(self.call_done_prefix + suffix):
            print("Waiting for call to finish..")
            time.sleep(5)

        return answered

