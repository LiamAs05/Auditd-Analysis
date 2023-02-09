
# Auditd Logs Analyzer
Created as an home assignment for the Magshimim + Cyngular Security job offer. This program will focus on analyzing syscalls by defining system call rules.

System call rules are added to auditd using the syntax: `auditctl -a action,filter -S system_call -F field=value -k key_name`
## Rule Setup

We will add the following auditd rule: `sudo auditctl -a always,exit -F arch=b64 -S fork`

A deeper understading of the command:

`"-a always" tells the auditd daemon to always log the syscalls`

`"exit" check if audit event needs to be created upon syscall exit`

`"-F arch=b-64" specifies that the rule is targeted for 64-bit system`

`"-S fork" specifies the rule targets "fork" syscall`

## Code Walkthorugh


The `AuditAnalyzer` class is where the log analysis happens. It has one attribute which is a constant and specifies the path of the audit log file.
```py
class AuditAnalyzer:
    def __init__(self):
        self._log_path = "/var/log/audit/audit.log"
```

The `DBManager` class uses `SQLModel` to interact with a local SQLite database. The path of the local database will always be the directory the main script is located at.  
```py
class DBManager:
    def __init__(self):
        db_path = join(dirname(abspath(__file__)), "logged_actions.sqlite")
        self._engine = create_engine("sqlite:///" + db_path)
        SQLModel.metadata.create_all(self._engine)
```

The `Action` class defines the parameters that are stored in the local database for each syscall.
```py
class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```
