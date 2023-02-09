from sqlmodel import Field, SQLModel, Session, create_engine
from os.path import dirname, abspath, join
from typing import Union

class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class DBManager:
    def __init__(self):
        db_path = join(dirname(abspath(__file__)), "logged_actions.sqlite")
        self._engine = create_engine("sqlite:///" + db_path)
        SQLModel.metadata.create_all(self._engine)
    
    def add_actions(actions: Union[Action, list[Action]]):
        if type(actions) == Action:     # if action is actually a single Action, convert it to a list
            actions = [actions]

        with Session(self._engine) as session:
            for action in actions:
                session.add(action)
            session.commit()

