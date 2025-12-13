import enum

class TodoStatus(enum.Enum):
    in_progress = "in-progress"
    completed = "completed"
    deleted = "deleted"