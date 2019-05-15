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

    def data_string(self, num):
        if num is not None:
            s = "&".join(["custom/tattle%d" % n for n in range(num)])
        else:
            s = "custom/tattle"

        s += "&yes-dear&get_bleep_outta&beep&beep&beep&beep&beep&silence/10&silence/10&silence/10"

        return s

    def write(self, num=None):
        tmphandle, tmppath = tempfile.mkstemp(text=True, suffix='.call')

        with os.fdopen(tmphandle, "w") as tmpfile:
            for fh in (tmpfile, sys.stdout):
                print("Channel: {}".format(self.extension), file=fh)
                print("CallerID: \"TATTLEPHONE\" <2>", file=fh)
                print("Application: playback", file=fh)
                print("Data: {}".format(self.data_string(num)), file=fh)
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
            return False

        print("Call answered")
        return True


