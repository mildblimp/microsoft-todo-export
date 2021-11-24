import json
import pypff
from bs4 import BeautifulSoup
import pandas as pd


def find_tasks_folder(root):
    for i, folder in enumerate(root.sub_folders):
        if folder.name == "Top of Personal Folders":
            for j, sub_folder in enumerate(folder.sub_folders):
                if sub_folder.name == "Tasks":
                    break
            break
    return root.sub_folders[i].sub_folders[j]


def get_subtasks(item):
    for en in item.record_sets[0].entries:
        try:
            output = en.data.decode("utf-16")
            if '{"Values":[' in output:
                output = json.loads(output)
                subtasks = [
                    {
                        "list": None,
                        "task": task["Subject"],
                        "description": None,
                        "creation_time": task["CreatedDateTime"],
                    }
                    for task in list(output.values())[0]
                ]
                return subtasks
        except (UnicodeDecodeError, AttributeError):
            pass
    return []


def recurse(folder, level=0):
    tasks = []
    for i, item in enumerate(folder.sub_items):
        if isinstance(item, pypff.folder):
            tasks.extend(recurse(item, level=level + 1))
        if isinstance(item, pypff.message):
            try:
                soup = BeautifulSoup(item.html_body, features="lxml")
                body = soup.body.div.string.rstrip()
            except (OSError, AttributeError, TypeError):
                body = None
            item_info = {
                "list": folder.name,
                "task": item.subject,
                "description": body,
                "creation_time": item.creation_time,
            }
            tasks.append(item_info)
            subtasks = get_subtasks(item)
            tasks.extend(subtasks)
    return tasks


if __name__ == "__main__":
    pst = pypff.file()
    pst.open("b2bbc2ea27cf40f5926338de537e4789.pst")
    root = pst.get_root_folder()
    # Recurse into the "Tasks" folder
    tasks_folder = find_tasks_folder(root)
    tasks = recurse(tasks_folder)
    pst.close()

    tasks = pd.DataFrame(tasks)
    print(tasks)
