import json
import pypff

pst = pypff.file()
pst.open("b2bbc2ea27cf40f5926338de537e4789.pst")


root = pst.get_root_folder()


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
                subtasks = [task["Subject"] for task in list(output.values())[0]]
                return subtasks
        except (UnicodeDecodeError, AttributeError):
            pass
    return []


def print_cutoff(idx, level, cutoff=5):
    if idx > cutoff:
        print("  " * level, "...")
        return True
    return False


def recurse(folder, level=0):
    for i, item in enumerate(folder.sub_items):
        if isinstance(item, pypff.folder):
            print("  " * level, item.name[:30])
            recurse(item, level=level + 1)
        if isinstance(item, pypff.message):
            # if item.subject in ["kvc opmerkingen", "Ikea"]:
            print("  " * level, item.subject)
            subtasks = get_subtasks(item)
            for j, task in enumerate(subtasks):
                print("  " * (level + 1), task)
                if print_cutoff(j, level + 1, cutoff=3):
                    break
            if print_cutoff(i, level):
                break


# Recurse into the "Tasks" folder
tasks_folder = find_tasks_folder(root)
recurse(tasks_folder)
pst.close()
