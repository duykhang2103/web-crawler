from apscheduler.schedulers.background import BackgroundScheduler
import json
import sys


from crawl.phongvu_selen import *
from crawl.phongvu_get_detail import *
# i = [0]

# def sensor(i):
#     i[0] += 1
#     print(i[0])

#     with open("static/json/1.json", "w", encoding ='utf8') as f:
#         json.dump(i[0], f, ensure_ascii=False, indent=4)

def s():
    saveData("./static/json/1.json", runProgram(urlList, tagNameList))
    getDetailPhongVu()

sched = BackgroundScheduler(daemon=True)
sched.add_job(s, trigger='interval', minutes=5)
sched.start()

# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

# def job():
#     print("Hello, world!")

# # Create a blocking scheduler
# scheduler = BlockingScheduler()

# # Add a job to run every 5 seconds using the default 'interval' trigger
# scheduler.add_job(job, 'interval', seconds=5)

# # Start the scheduler
# scheduler.start()

# # Create a background scheduler
# background_scheduler = BackgroundScheduler()

# # Add a job to run every 5 seconds using the default 'interval' trigger
# background_scheduler.add_job(job, 'interval', seconds=5)

# # Start the scheduler in the background
# background_scheduler.start()

# # Keep the main thread alive while the background scheduler runs
# try:
#     while True:
#         pass
# except KeyboardInterrupt:
#     pass

# # Shut down the background scheduler when the main thread is interrupted
# background_scheduler.shutdown()