from typing import List, Set, TypedDict
from datetime import datetime
from __future__ import annotations
class BaseTask(TypedDict):
    content: str
    start_ts: str
    end_ts: str
    tags: Set[BaseTask]
    completed: bool
    created_ts: datetime.datetime
    


def create_task():
    new_task = BaseTask()
    print(new_task)



if __name__ == "main":
    create_task()