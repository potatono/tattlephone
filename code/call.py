import os
import config
import tempfile
import shutil

class Call:
    def __init__():
        self.recording = config.tattle_drop_name
        self.waittime = config.phone_ring_wait_time
        self.extension = config.phone_channel
        self.call_exec_path = config.call_spool_path

    def write():
        tmphandle, tmppath = tempfile.mkstemp(text=True, suffix='.call')

        with os.fdopen(tmphandle, "w") as tmpfile:
            print("Channel: {}".format(self.extension), file=tmpfile)
            print("Application: playback", file=tmpfile)
            print("Data: {}".format(self.recording), file=tmpfile)
            print("WaitTime: {}".format(self.waittime), file=tmpfile)

        return tmppath

    def execute(callpath):
        shutil.move(callpath, self.call_exec_path)


