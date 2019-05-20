import os

tz = 'America/New_York'
tattle_extension = 2
tattle_duration = 15

phone_extension = 204
phone_protocol = "PJSIP"
phone_channel = os.path.join(phone_protocol, str(phone_extension))
phone_ring_wait_time = 15

spool_path = "/var/spool/asterisk"
lib_path = "/var/lib/asterisk"

tattle_vm_inbox_path = os.path.join(spool_path, 'voicemail', 'default',
                              str(tattle_extension), 'INBOX')
tattle_vm_old_path = os.path.join(spool_path, 'voicemail', 'default',
                              str(tattle_extension), 'Old')

tattle_drop_name = 'custom/tattle1'
tattle_drop_path = os.path.join(lib_path, 'sounds', 'en', 'custom',
                                'tattle.wav')

call_spool_prefix = os.path.join(spool_path, 'outgoing', 'tattle')
call_spool_outgoing_prefix = os.path.join(spool_path, 'outgoing_done', 'tattle')

calling_hours = ((11, 23),)
call_mins_after_tattle = 3/60
call_mins_after_answer = 60
call_mins_after_no_answer = 10
