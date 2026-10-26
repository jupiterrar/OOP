from typing import List, Optional, Protocol
from typing import Literal
from dataclasses import dataclass
import datetime
import uuid

task_status_type = Literal['todo', 'in_progress', 'done']
task_status = ('todo', 'in_progress', 'done')

@dataclass(frozen=True) #для себя: dataclass нужен, чтобы не писать инит и тд. фроузен - нельзя менять
class Task():
    id: str
    title: str
    status: task_status_type
    created_at: datetime
    tags: list[str]
    priority: int = 3

    def __post_init__(self):
        if not isinstance(self.id, str):
            raise ValueError("Invalid data type. ID must be a string.")
        try:
            parsed_uuid = uuid.UUID(self.id)
            if parsed_uuid.version != 4:
                raise ValueError("Invalid UUID version. It must be UUID4.")
        except ValueError as e:
            raise ValueError("Invalid UUID string.") from e

        if not isinstance(self.title, str):
            raise ValueError("Invalid data type. Title must be a string.")
        if not 1 <= len(self.title) <= 200:
            raise ValueError("Title must contain 1-200 characters.")

        if self.status not in task_status:
            raise ValueError("Invalid data type. Task status must be 'todo', 'in_progress' or 'done'.")

        if not isinstance(self.created_at, datetime.datetime):
            raise ValueError("Invalid data type. Created_at must be a datetime object.")

        if not isinstance(self.tags, list) or not all(isinstance(t, str) for t in self.tags):
            raise ValueError("Invalid data type. Tags must be a list of strings.")

        if not isinstance(self.priority, int):
            raise ValueError("Invalid data type. Priority should be a number")
        if not (1 <= self.priority <= 5): 
            raise ValueError("Priority should be from 1 to 5.")

    def create():
        pass

    def read():
        pass

@dataclass(frozen=True)
class TaskFilter():
    status: Optional[task_status_type] = None
    tag: Optional[str] = None
    min_priority: Optional[int] = None

    def match(self, task: Task) -> bool:
        if self.status and task.status != self.status:
            return False
        if self.tag and self.tag not in task.tags:
            return False
        if self.min_priority and (task.priority < 1 or task.priority > 5):
            return False
        return True


class Storage(Protocol):
    def save(self, task: Task) -> None:
        ...
    def get(self, task_id: str) -> Task:
        ...
    def delete(self, task_id: Task) -> None:
        ...
    def list_all(self, filter: Optional[TaskFilter] = None) -> List[Task]:
        ...

class TaskNotFound(Exception): pass
class DuplicateTaskId(Exception): pass
class StorageError(Exception): pass

class InMemoryRepository():
    def __init__(self):
        self.tasks = []

    def save(self, task: Task) -> None:
        for existing_task in self.tasks:
            if existing_task.id == task.id:
                raise DuplicateTaskId("This task already exists.")
        self.tasks.append(task)

    def get(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound("Task not found.")

    def delete(self, task_id: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return
        raise TaskNotFound("Task not found.")

    def list_all(self, filter: Optional[TaskFilter] = None) -> List[Task]:
        if filter is None:
            return self.tasks
        
        filtered_tasks = []
        for task in self.tasks:
            if filter.match(task):
                filtered_tasks.append(task)
        return filtered_tasks

if __name__ == "__main__":
    valid_id = str(uuid.uuid4())
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    park = Task(valid_id, 'Park', 'todo', utc_now, ['home', 'work'], 3)

    valid_id = str(uuid.uuid4())
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    home = Task(valid_id, 'Home', 'todo', utc_now, ['home'], 3)
    
    repo = InMemoryRepository()

    repo.save(park)
    repo.save(home)
    print("Все задачи в хранилище:", repo.list_all())

    my_filter = TaskFilter(tag='work')
    print("Отфильтрованные задачи:", repo.list_all(filter=my_filter))