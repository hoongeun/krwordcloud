import datetime


categories = ["economy", "society", "culture", "it"]
procs = 12
queue_size = 100
time_to_live = 10620  # 3 hours - 3minutes(to clear the job)
KST = datetime.timezone(datetime.timedelta(hours=9))
min_date = datetime.datetime(2010, 1, 1, tzinfo=KST)
