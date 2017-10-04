import schedule
import time
from threading import Thread

from app.services.cron import JOBS


def job():
    print("I'm working..." + str(time.time()))


def post_feed_job():
    schedule.every(5).seconds.do(job)


def schedule_timer():
    while True:
        schedule.run_pending()
        time.sleep(1)

# run cron job


def run_schedule():
    if (len(JOBS) <= 0):
        t = Thread(target=schedule_timer)
        post_feed_job()
        t.start()
        JOBS.append(1)
