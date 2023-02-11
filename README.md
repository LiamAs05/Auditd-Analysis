
# Auditd Logs Analyzer
Created as an home assignment for the Magshimim + Cyngular Security job offer. This program will focus on analyzing syscalls by defining system call rules.

The main focus of the code will be comparing between four syscalls: `kill, execve, fork, chdir`. I will analyze which one is called more times, by which user, etc.


## Auditd Setup

First, install auditd and useful plugins by running (Debian):
`sudo apt-get install auditd audispd-plugins`

To start auditd: `service auditd start`

To stop auditd: `service auditd stop`

To fetch the current status of auditd: `service auditd status`

To view all current rules: `sudo auditctl -l`

Log files are stored at `/var/log/audit/audit.log` (can be changed in `/etc/audit/auditd.conf`)
## Rule Setup

System call rules are added to auditd using the syntax: `auditctl -a action,filter -S system_call -F field=value -k key_name`

We will add the following auditd rule: `sudo auditctl -a always,exit -F arch=b64 -S kill -S fork -S execve -S chdir -k SPECIAL_CALL`

A deeper understading of the command:

`"-a always" tells the auditd daemon to always log the syscalls`

`"exit" check if audit event needs to be created upon syscall exit (evaluates all syscalls)`

`"-F arch=b-64" specifies that the rule is targeted for 64-bit system`

`"-s KILL -S fork -S execve -S chdir" specifies the syscalls to audit`

`"-k SPECIAL_CALL" tells all related audits to be marked with the SPECIAL_CALL key`

To start tracking, we will preform the following chain of commands:
`sudo service auditd stop; sudo rm /var/log/audit/audit.log; sudo service auditd start; sudo auditctl -a always,exit -F arch=b64 -S kill -S fork -S execve -S chdir -k SPECIAL_CALL`

This will stop the daemon if it is currently running, delete previous logs, start the daemon and create the rule we wished for. It is optional to run `sudo service auditd status` and `sudo auditctl -l` to make sure the operation succeeded.
## Code Walkthorugh


The `AuditAnalyzer` class is where the log analysis happens. It has one attribute which is a constant and specifies the path of the audit log file.
```py
class AuditAnalyzer:
    def __init__(self, log_path: str = None):
        self._log_path = "/var/log/audit/audit.log" if not log_path else log_path
        ...
        self.read_logs()
        self.filter_logs()
        self.parse_actions()
```

The imporant functions in this class are `filter_logs` and `parse_actions`.
`filter_logs` splits the lines in the auditd log file by syscall using the python `filter` function.

```py
def filter_logs(self) -> None:
            self._filtered_logs = self._filtered_logs.split(SEPERATOR)
            self._filtered_logs = list(filter(lambda s: KEY 
            in s and IS_CONFIG_RELATED not in s, self._filtered_logs))
```

`parse_actions` uses the filtered logs and picks the important information. It tracks the syscall that has been called, the caller username and the exit status (success/failure). It's code is mostly technical and involves a lot of string parsing with `split, rsplit, resplit, index [::], etc`.


The `DBManager` class uses `SQLModel` to interact with a local SQLite database. The path of the local database will always be the directory the main script is located at.  

```py
class DBManager:
    def __init__(self):
        db_path = join(dirname(abspath(__file__)), "logged_actions.sqlite")
        with open(db_path, "w"):
            pass    # clearing the current database
        self._engine = create_engine("sqlite:///" + db_path)
        SQLModel.metadata.create_all(self._engine)
```

The `Action` class defines the parameters that are stored in the local database for each syscall.
```py
class Actions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    syscall_type: str = Field(default=None)
    calling_user: str = Field(default=None)    
    success: int = Field(default=None)
```

The connection with the database is created upon the creation of an instance. Reading and writing to the database is done by the writing function `add_actions` and three similar reading functions, each responsible for a property of the `Actions` class.

For example, `get_users` reads all of the users that performed a syscall from the DB and returns a dictionary with the usernames as keys and the amount of syscalls as values.
```py
def get_users(self) -> dict[str, int]:
        users_dict = {}
        with Session(self._engine) as session:
            statement = select(Actions.calling_user)
            for user in session.exec(statement):
                if users_dict.get(user, None) == None:
                    users_dict[user] = 0
                else:
                    users_dict[user] += 1

        return users_dict
``` 

The `Visualizer` class contains a single static method that uses matplotlib's plt to create a pie diagram. This allows us to visualize the distribution of the syscalls nicely.
```p
@staticmethod
def visualize(syscalls: list[str]) -> None:
    labels = 'fork', 'kill', 'chdir', 'execve'
    sizes = [0, 0, 0, 0]
    for syscall in syscalls:
        for label in labels:
            if syscall == label:
                sizes[labels.index(label)] += 1
                break

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
```
