from __future__ import annotations
from typing import List, Set, TypedDict
from datetime import datetime
class BaseTask(TypedDict):
    content: str
    start_ts: str
    end_ts: str
    tags: Set[BaseTask]
    completed: bool
    created_ts: datetime.datetime
    


def create_task():
    for value in BaseTask.items:
        print(value)



if __name__ == "main":
    create_task()