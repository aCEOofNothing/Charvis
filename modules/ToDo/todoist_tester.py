from modules.ToDo.Todoist import TodoistAdapter
todo = TodoistAdapter("6d619c5598e512c9b8c4ec54609353b19bcec942")
print(todo.add_task("Geil! klappt!", due="tomorrow", priority=4))
print(todo.list_tasks())