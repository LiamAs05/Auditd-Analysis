from sqlmodel import Field, SQLModel, Session, create_engine
from os.path import dirname, abspath, join
from enum import Enum
from typing import Optional

class Syscall(Enum):
    FORK = "fork"
    EXECVE = "execve"
    CHDIR = "chdir"
    KILL = "kill"

class Actions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    syscall_type: str = Field(default=None)
    calling_user: str = Field(default=None)    
    success: int = Field(default=None)

class DBManager:
    def __init__(self):
        db_path = join(dirname(abspath(__file__)), "logged_actions.sqlite")
        with open(db_path, "w"):
            pass    # clearing the current database
        self._engine = create_engine("sqlite:///" + db_path)
        SQLModel.metadata.create_all(self._engine)

    def add_actions(self, actions: list[Actions]):
        with Session(self._engine) as session:
            for action in actions:
                session.add(action)
            session.commit()

