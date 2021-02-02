
from feeder import load_table
from apscheduler.schedulers.background import BlockingScheduler
from analysis import do_analysis
from webserver import start_server

if __name__ == '__main__':        
         
          sched = BlockingScheduler()          
          sched.add_job(load_table, 'interval', seconds =1800)
          sched.add_job(do_analysis,'cron',day_of_week='mon-fri',hour=00,minute=00)
          sched.add_job(start_server,'cron',day_of_week='mon-fri',hour=00,minute=30)
          sched.start()

