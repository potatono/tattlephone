from voicemails import Voicemails
from call import Call

vms = Voicemails()
call = Call()

vms.read()
print(vms.voicemails)
vms.filter()
vms = vms.shuffled()
num = min(len(vms), 1)
for i in range(num):
    vms[i].prep_playback(i)

print("Playing %d tattles.." % num)
path = call.write(num)
call.execute(path)
print(path)

