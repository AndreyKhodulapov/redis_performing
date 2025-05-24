import json
import threading

import flet as ft

from app_redis_client import get_redis

redis_client = get_redis()

tasks ={}

def main(page: ft.Page):
    page.title = "Task tracker on Redis"

    task_input = ft.TextField(label="Enter the task", width=300)

    task_list = ft.Column()

    def add_task(e):
        task_name = task_input.value.strip()
        if not task_name:
            return

        task_id = f"task:{task_name}"
        tasks[task_id] = ft.Text(f"{task_name} - Waiting", color="grey")

        redis_client.lpush("task_queue", json.dumps({
            "id": task_id,
            "name": task_name
        }))

        redis_client.hset(task_id, "status", "pending")

        task_list.controls.append(tasks[task_id])

        task_input.value = ""
        page.update()

    def listen_for_updates():
        pubsub = redis_client.pubsub()
        pubsub.subscribe("task_status_channel")

        for message in pubsub.listen():
            if message["type"] == "message":
                status_update = json.loads(message["data"])
                task_id = status_update["task_id"]
                status = status_update["status"]

                if task_id in tasks:
                    tasks[task_id].color = "green" if status == "completed" else "red"
                    tasks[task_id].value = f"{task_id.split(':')[1]} - {status.upper()}"
                    page.update()

    add_button = ft.ElevatedButton("Add", on_click=add_task)

    page.add(task_input, add_button, task_list)

    threading.Thread(target=listen_for_updates, daemon=True).start()


ft.app(main)