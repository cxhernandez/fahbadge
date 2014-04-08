from apscheduler.scheduler import Scheduler
import urllib2

__DB__ = 'http://fah-web.stanford.edu/daily_user_summary.txt.bz2';

sched = Scheduler()

@sched.interval_schedulem(minutes=30)
def timed_job():
    print 'Getting database...'
    

sched.start()

while True:
    pass