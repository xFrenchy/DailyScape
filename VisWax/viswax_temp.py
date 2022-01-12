from datetime import date, timedelta
from GID_Historic import GID_Historic
from GID import GID

today = date.today()
past_date = today - timedelta(days=40)

#Test only
today = date(2021, 3, 28)
yesterday = today - timedelta(days=1)
past_date = today - timedelta(days=40)
before_past_date = today - timedelta(days=41)

# yes +- X = today
# 41 - 40 = Y

diff1 = GID_Historic[date.isoformat(before_past_date)]
diff2 = GID_Historic[date.isoformat(past_date)]

difference = abs(abs(diff1 - diff2) - GID_Historic[date.isoformat(yesterday)])

today_GID = GID_Historic[date.isoformat(yesterday)] - (abs(diff1 - diff2))

print("Slot 1 for ", today, " is: ", GID[today_GID])