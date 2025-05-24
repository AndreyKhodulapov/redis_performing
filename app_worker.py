import time
import json

from app_redis_client import get_redis

redis_client = get_redis()

def update_status(task_id, status):
    redis_client.hset(task_id, "status", status)

    redis_client.publish("task_status_channel", json.dumps({
        "task_id": task_id,
        "status": status
    }))

def process_task(task):
    task_id = task["id"]

    update_status(task_id, "in_progress")

    time.sleep(3)

    update_status(task_id, "completed")

def main():
    print("Start worker")

    while True:
        _, task_data = redis_client.brpop("task_queue")

        task = json.loads(task_data)

        process_task(task)

if __name__ == "__main__":
    main()