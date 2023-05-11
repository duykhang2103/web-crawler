from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print("Hello, world!")

# Create a blocking scheduler
scheduler = BlockingScheduler()

# Add a job to run every 5 seconds using the default 'interval' trigger
scheduler.add_job(job, 'interval', seconds=5)

# Start the scheduler
scheduler.start()

# Create a background scheduler
background_scheduler = BackgroundScheduler()

# Add a job to run every 5 seconds using the default 'interval' trigger
background_scheduler.add_job(job, 'interval', seconds=5)

# Start the scheduler in the background
background_scheduler.start()

# Keep the main thread alive while the background scheduler runs
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Shut down the background scheduler when the main thread is interrupted
background_scheduler.shutdown()