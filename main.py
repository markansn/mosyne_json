from __future__ import annotations
from typing import List, Optional, Set, TypedDict
from datetime import datetime, date, timezone
from dateutil.parser import parse
import json
from dateutil.parser import ParserError
import os
from glob import glob
import pytz
import pandas as pd 
FILES_LOC = "files/"
class BaseTask(TypedDict):
    content: str
    start_ts: Optional[datetime.datetime]
    end_ts: Optional[datetime.datetime]
    tags: Optional[datetime.datetime]
    completed: bool
    created_ts: datetime.datetime
    modified_ts: datetime.datetime
    

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def input_with_mosyne_tag(extension: Optional[str] = None):
    if extension:
        return input(f"mosyne [{extension}]> ")
    else:
        return input("mosyne> ")

def get_input(msg: str, is_optional: bool = True):
    while True:
        result = input_with_mosyne_tag(msg)
        if result == "":
            if is_optional:
                return None
            else:
                print("You must provide a value")
        else:
            return result

def get_date(date_type: str):
    while True:
        if date_type == "start_ts":
            result = get_input("start")
        elif date_type == "end_ts":
            result = get_input("end")
        else:
            return RuntimeError(f"Unknown date type {msg}")
        if result is not None:
            try:
                parsed = parse(result, fuzzy=True, dayfirst=True)
                parsed = parsed.replace(tzinfo=pytz.timezone("Europe/London"))
                print(parsed)
            except ParserError:
                print(f"Could not parse date string {result}, please try again")
            else:
                return parsed
        else:
            return None

def get_tags():
    tags_string = get_input("tags")
    if tags_string is None: 
        return []
    tags = tags_string.split(",")
    out = []
    for tag in tags:
        out.append(tag.strip())
    return out

def create_task():
    new_task = BaseTask()
    new_task["content"] = get_input("task name", is_optional=False)
    new_task["start_ts"] = get_date("start_ts")
    new_task["end_ts"] = get_date("end_ts")
    new_task["tags"] = get_tags()
    new_task["created_ts"] = datetime.now(tz=datetime.now(timezone.utc).astimezone().tzinfo)
    new_task["modified_ts"] = None
    new_task["completed"] = False

    
    return new_task

def save_task(task: BaseTask):
    with open(os.path.join(FILES_LOC, f"{task['content']}.json"), "w+") as f:
        f.write(json.dumps(task, default=json_serial, indent=4, sort_keys=True))
    

def load_tasks():
    tasks = []
    for file_path in glob(f"{FILES_LOC}/*.json"):
        print("loading", file_path)
        with open(file_path, "r") as f:
            d = json.load(f)
        d["created_ts"] = datetime.fromisoformat(d["created_ts"])
        tasks.append(d)  
    return pd.DataFrame(tasks)

def cli():
    task_df = load_tasks()
    while True:
        line = input_with_mosyne_tag().strip()
        if line == "new":
            task = create_task()
            print(f"created new task: {task}")
            save_task(task)
        if line == "show":
            with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
                print(task_df.filter(items=["content, "]))

cli()