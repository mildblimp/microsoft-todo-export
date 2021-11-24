import argparse
import json

import pandas as pd
import pypff
from bs4 import BeautifulSoup


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
    parser = argparse.ArgumentParser(
        description="Export tasks from a Microsoft To Do pst file to csv."
    )
    parser.add_argument("infile", type=argparse.FileType("r"), help="input file (.pst)")
    parser.add_argument(
        "-o",
        "--outfile",
        nargs="?",
        type=argparse.FileType("w"),
        help="output file (.csv)",
    )
    args = parser.parse_args()
    pst = pypff.file()
    pst.open(args.infile.name)
    root = pst.get_root_folder()
    tasks_folder = find_tasks_folder(root)
    tasks = recurse(tasks_folder)
    pst.close()

    tasks = pd.DataFrame(tasks)
    if args.output_file is None:
        print(tasks)
    else:
        tasks.to_csv(args.output_file, index=False)
