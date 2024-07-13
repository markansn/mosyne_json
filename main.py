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
import sqlite3
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
    tasks = set()
    for file_path in glob(f"{FILES_LOC}/*.json"):
        print("loading", file_path)
        with open(file_path, "r") as f:
            d = json.load(f)
        d["created_ts"] = datetime.fromisoformat(d["created_ts"])
        tasks.add(d)  
    return tasks

def generate_sql_db(task: BaseTask):
    print("Generating db")
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute("create table tasks(content, start_ts, end_ts, tags, created_ts, modified_ts, completed)")
    cur.execute(f"insert into test values ({task['content']}, {task['start_ts']}, {task['end_ts']}, {task['tags']}, {task['created_ts']}, {task['modified_ts']}, {task['completed']})")
    result = cur.execute("SELECT * from test")
    print(result.fetchone())

def cli():
    task_set = load_tasks()
    
    while True:
        line = input_with_mosyne_tag().strip()
        if line == "new":
            task = create_task()
            print(f"created new task: {task}")
            save_task(task)
        if line == "show":
            with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
                print(task_df.filter(items=["content, "]))

# cli()
generate_sql_db(create_task())