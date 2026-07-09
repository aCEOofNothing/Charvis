
import requests



class TodoistAdapter:
    def __init__(self, token):
        self.token = token
        self.base = "https://api.todoist.com/v1"
        self.headers = {"Authorization": f"Bearer {token}"}

    def add_task(self, content, due=None, priority=1):
        data = {"content": content, "priority": priority}
        if due:
            data["due_string"] = due

        r = requests.post(self.base + "/tasks", json=data, headers=self.headers)
        return r.text

def list_tasks(self):
    r = requests.get(self.base + "/tasks", headers=self.headers)

    print("STATUS:", r.status_code)
    print("TEXT:", r.text)

    try:
        return r.json()
    except:
        return {"error": r.text}

    def delete_task(self, task_id):
        r = requests.delete(f"{self.base}/tasks/{task_id}", headers=self.headers)
        return r.text