import os

tattle_extension = 2

phone_extension = 204
phone_protocol = "PJSIP"
phone_channel = os.path.join(phone_protocol, str(phone_extension))
phone_ring_wait_time = 15

spool_path = "/var/spool/asterisk"
lib_path = "/var/lib/asterisk"

tattle_vm_path = os.path.join(spool_path, 'voicemail', 'default',
                              str(tattle_extension), 'INBOX')

tattle_drop_name = 'custom/tattle1'
tattle_drop_path = os.path.join(lib_path, 'sounds', 'en', 'custom',
                                'tattle.wav')

call_spool_prefix = os.path.join(spool_path, 'outgoing', 'tattle')
call_spool_outgoing_prefix = os.path.join(spool_path, 'outgoing_done', 'tattle')

calling_hours = ((21, 23),)
calling_idle_time = 20
