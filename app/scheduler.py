from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from app.pipeline.run_pipeline import run_pipeline

# Prevent overlapping runs
executors = {
    "default": ThreadPoolExecutor(max_workers=1)
}

jobstores = {
    "default": MemoryJobStore()
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    timezone="UTC"
)

def start_scheduler():
    # Run every 30 minutes (change later if needed)
    scheduler.add_job(
        run_pipeline,
        trigger="interval",
        minutes=30,
        id="pipeline_job",
        replace_existing=True,
        kwargs={"trigger": "scheduler"}
    )

    scheduler.start()
    print("⏱️ Scheduler started (every 30 minutes)")