import argparse
import json
import logging
from datetime import datetime


from __init__ import __version__


logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s: %(message)s")

def get_parser():
    """构建程序命令行参数"""
    parser = argparse.ArgumentParser(description="A cli task-tracker!",
                                     prog="task-tracker",
                                     conflict_handler="error",
                                     epilog="Enjoy the program! :)")
    parser.add_argument("-V", "--version")
    
    # required 要求必须使用子命令
    subparsers = parser.add_subparsers(dest="subcommamd", 
                                       help="sub-commands", 
                                    #    required=True
                                    )
    
    add_parser = subparsers.add_parser("add", help="add a task")
    add_parser.add_argument("task", 
                            help="the task content")
    add_parser.add_argument("-d", 
                            "--description", 
                            help="the task description", 
                            default="")
    add_parser.add_argument("-p", 
                            "--priority", 
                            help="the task priority", 
                            default="medium")
    add_parser.add_argument("-s", 
                            "--status", 
                            help="the task status", 
                            default="todo")
    
    delete_parser = subparsers.add_parser("delete", help="delete a task")
    delete_parser.add_argument("task_id", 
                               help="the task id")
    
    update_parser = subparsers.add_parser("update", help="update a task")
    update_parser.add_argument("task_id", 
                               help="the task id")
    update_parser.add_argument("-t", 
                               "--task", 
                               help="the task content")
    update_parser.add_argument("-d", 
                               "--description", 
                               help="the task description")
    update_parser.add_argument("-p", 
                               "--priority", 
                               help="the task priority")
    update_parser.add_argument("-s", 
                               "--status", 
                               help="the task status")
    
    list_parser = subparsers.add_parser("list", help="list tasks")
    list_parser.add_argument("--all", 
                             help="list all tasks", 
                             action="store_true")
    list_parser.add_argument("-s", 
                             "--status", 
                             help="the task status")
    list_parser.add_argument("-p", 
                             "--priority", 
                             help="the task priority")
    
    mark_done_parser = subparsers.add_parser("mark_done", help="mark a task as done")
    mark_done_parser.add_argument("task_id", 
                                  help="the task id")
    
    mark_pending_parser = subparsers.add_parser("mark_pending", help="mark a task as pending")
    mark_pending_parser.add_argument("task_id", 
                                     help="the task id")
    
    return parser


def run_cli():
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        with open("tasks.json", "w") as f:
            f.write("[]")
        tasks = []    
    except json.JSONDecodeError:
        logger.error("Error: Failed to decode JSON from tasks.json")
        return
    except Exception as e:
        logger.error(e)
        return
        
    parser = get_parser()
    try:
        args = vars(parser.parse_args())
    except Exception as e:
        logger.error(e)
        return
    
    if args['version']:
        print(__version__)
        return
    
    try:
        if args["subcommamd"] == "add":
            task = {
                "id": len(tasks) + 1,
                "task": args["task"],
                "description": args["description"],
                "priority": args["priority"],
                "status": args["status"],
                "createdAt": datetime.now().isoformat(sep=" ", timespec="seconds"),
                "updatedAt": datetime.now().isoformat(sep=" ", timespec="seconds")
            }
            tasks.append(task)
            with open(".tasks.json", "w") as f:
                json.dump(tasks, f)
        elif args["subcommamd"] == "delete":
            task_id = int(args["task_id"])
            tasks = [task for task in tasks if task["id"] != task_id]
            for new_id, task in enumerate(tasks):
                task["id"] = new_id
            with open(".tasks.json", "w") as f:
                json.dump(tasks, f)
        elif args["subcommamd"] == "update":
            task_id = int(args["task_id"])
            for task in tasks:
                if task["id"] == task_id:
                    task["task"] = args["task"] or task["task"]
                    task["description"] = args["description"] or task["description"]
                    task["priority"] = args["priority"] or task["priority"]
                    task["status"] = args["status"] or task["status"]
                    task["updatedAt"] = datetime.now().isoformat(sep=" ", timespec="seconds")
            with open(".tasks.json", "w") as f:
                json.dump(tasks, f)
        elif args["subcommamd"] == "list":
            if args["all"]: # true or false
                for task in tasks:
                    print(f"{task['id']}: {task['task']} --- {task['description']} --- {task['status']}")
            elif args["status"]: # str or None
                for task in tasks:
                    if task["status"] == args["status"]:
                        print(f"{task['id']}: {task['task']} --- {task['description']} --- {task['status']}")
            elif args["priority"]: # str or None
                for task in tasks:
                    if task["priority"] == args["priority"]:
                        print(f"{task['id']}: {task['task']} --- {task['description']} --- {task['status']}")
        elif args['subcommamd'] == "mark_done":
            task_id = int(args["task_id"])
            for task in tasks:
                if task["id"] == task_id:
                    task["status"] = "done"
                    task["updatedAt"] = datetime.now().isoformat(sep=" ", timespec="seconds")
            with open(".tasks.json", "w") as f: 
                json.dump(tasks, f)
        elif args['subcommamd'] == "mark_pending":
            task_id = int(args["task_id"])
            for task in tasks:
                if task["id"] == task_id:
                    task["status"] = "todo"
                    task["updatedAt"] = datetime.now().isoformat(sep=" ", timespec="seconds")
            with open(".tasks.json", "w") as f:
                json.dump(tasks, f)
        else:
            pass
    except Exception as e:
        logger.error(e)
        return
    
    print("Done!")

if __name__ == "__main__":
    run_cli()
