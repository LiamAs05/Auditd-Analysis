from sqlmodel import Field, SQLModel, Session, create_engine, select
from os.path import dirname, abspath, join
from enum import Enum
from typing import Optional


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

    def add_actions(self, actions: list[Actions]) -> None:
        """
        This function addes the syscalls to the syscall database
        @param actions The syscalls logged in the auditd log file
        @return None
        """
        with Session(self._engine) as session:
            for action in actions:
                session.add(action)
            session.commit()
    
    def get_syscalls(self) -> list[str]:
        """
        This function returns all of the syscalls in the database
        @return list of syscalls
        """
        with Session(self._engine) as session:
            statement = select(Actions.syscall_type)
            return [action for action in session.exec(statement)]

    def get_status(self) -> dict[int, int]:
        """
        This function returns a dict; 1=success, 0=failure
        {0: times of failure, 1: times of success}
        @rtype dict
        """
        status_dict = {0: 0, 1: 0}
        with Session(self._engine) as session:
            statement = select(Actions.success)
            for status in session.exec(statement):
                status_dict[status] += 1

        return status_dict

    def get_users(self) -> dict[str, int]:
        """
        Similar to the two functions defined above,
        this time returning a dict of {username: num of calls}
        @rtype: dict[str, int]
        """
        users_dict = {}
        with Session(self._engine) as session:
            statement = select(Actions.calling_user)
            for user in session.exec(statement):
                if users_dict.get(user, None) == None:
                    users_dict[user] = 0
                else:
                    users_dict[user] += 1

        return users_dict
