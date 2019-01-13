import Reminder_Funcs as RF
import schedule
import time

# Google Keep login credentials
email = ''
password = ''

# Twilio credentials
phone_num = ''
twilio_num = ''
account_sid = ''
auth_token = ''

# Time the reminder text is sent
run_time = '08:30'


# send reminder text at your specified time
schedule.every().day.at(run_time).do(RF.remind, email, password, phone_num, twilio_num, account_sid, auth_token)

#
while 1:
    schedule.run_pending()
    time.sleep(1)