from apscheduler.schedulers.background import BackgroundScheduler
import json
import sys

from crawl.phongvu_get_detail import *
from crawl.gearvn_get_detail import *
from crawl.tgdd_get_detail import *
from crawl.cellphones_get_detail import *

def s():
    startCellphoneS()
    startTgdd()
    startPhongVu()
    startGearvn()

sched = BackgroundScheduler(daemon=True)
sched.add_job(s, trigger='interval', days=1)
sched.start()
