from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

def my_scheduled_job():
    logger.info("This is a scheduled job running...")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        my_scheduled_job,
        trigger=CronTrigger(hour="14", minute="30"),  # Runs daily at 2:30 PM
        id="payments_scheduler",  # Unique ID for the job
        replace_existing=True,  # Replace existing job with the same ID
    )
    scheduler.start()
    logger.info("Scheduler started!")
