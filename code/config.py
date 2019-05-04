import os

tattle_extension = 2

phone_extension = 204
phone_protocol = "PJSIP"
phone_channel = os.path.join(phone_protocol, phone_extension)
phone_ring_wait_time = 10

spool_path = "/var/spool/asterisk"
lib_path = "/var/lib/asterisk"

tattle_vm_path = os.path.join(spool_path, 'voicemail', 'default',
                              str(tattle_extension), 'INBOX')

tattle_drop_name = 'current-tattle'
tattle_drop_path = os.path.join(lib_path, 'sounds', 'en',
                                'current-tattle.wav')

call_spool_path = os.path.join(spool_path, 'outgoing', 'tattle.call)
