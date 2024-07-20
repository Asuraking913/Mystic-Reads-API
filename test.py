from datetime import datetime

current_datetime = datetime.now()
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day
current_time = current_datetime.time()

print("Current Year:", current_year)
print("Current Month:", current_month)
print("Current Day:", current_day)
print("Current time:", current_time.minute)
