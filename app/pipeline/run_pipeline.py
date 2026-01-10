from datetime import datetime

def run_pipeline(trigger="manual"):
    """
    Scheduler-safe placeholder.
    Real analysis is triggered via Telegram /analyze command.
    """

    start_time = datetime.utcnow()

    print("========== PIPELINE START ==========")
    print(f"Trigger     : {trigger}")
    print(f"Started at  : {start_time}")

    # Intentionally empty for now
    # Real execution happens via /analyze

    end_time = datetime.utcnow()
    print(f"Ended at    : {end_time}")
    print("=========== PIPELINE END ===========")

    return {
        "status": "idle",
        "trigger": trigger,
        "started_at": start_time.isoformat(),
        "ended_at": end_time.isoformat()
    }
