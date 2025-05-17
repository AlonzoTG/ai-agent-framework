#!/usr/bin/env python3
import time
import requests

# Change if your API is on a different host/port
BASE_URL = "http://127.0.0.1:8000"

def get_tasks():
    resp = requests.get(f"{BASE_URL}/tasks/")
    resp.raise_for_status()
    return resp.json()

def get_task(task_id):
    resp = requests.get(f"{BASE_URL}/tasks/{task_id}")
    resp.raise_for_status()
    return resp.json()

def update_task(task_obj):
    resp = requests.put(f"{BASE_URL}/tasks/{task_obj['id']}", json=task_obj)
    resp.raise_for_status()
    return resp.json()

def main(poll_interval=5):
    print("[Agent] Starting poller (Ctrl-C to stop)…")
    while True:
        try:
            tasks = get_tasks()
            # find the first task not yet done
            for t in tasks:
                if t.get("status") != "done":
                    print(f"[Agent] Picked task {t['id']}: {t['title']}")
                    # fetch full object to ensure required fields
                    task = get_task(t["id"])
                    task["status"] = "done"
                    updated = update_task(task)
                    print(f"[Agent] Marked {updated['id']} as done.")
                    break
            else:
                print("[Agent] No pending tasks.")
        except Exception as e:
            print(f"[Agent] Error: {e}")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
