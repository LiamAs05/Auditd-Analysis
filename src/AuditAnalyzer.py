from sys import stderr
from DBManager import Actions
from re import split as resplit

USER_SEPARATOR = "UID"
SUCCESS_SEPARATOR = "success"
SYSCALL_SEPARATOR = "SYSCALL"
KEY = "SPECIAL_CALL"
IS_CONFIG_RELATED = "CONFIG"
SEPERATOR = "type"
NO_FILE = -3
BAD_PARSE = -4

class AuditAnalyzer:
    def __init__(self, log_path: str = None):
        """ 
        the path specified below is the default log file path
        although the user can pass another log path if he wants to.
        """
        self._log_path = "/var/log/audit/audit.log" if not log_path else log_path
        self._filtered_logs = None
        self._actions = []
        self.read_logs()
        self.filter_logs()
        self.parse_actions()

    def read_logs(self) -> None:
        """
        This function reads the log file
        @return None
        """
        try:
            with open(self._log_path, "r") as log_file:
                self._filtered_logs = log_file.read()
        except FileNotFoundError:
            print("Your system does not contain a log file", file=stderr)
            exit(NO_FILE)

    def filter_logs(self) -> None:
        """
        This function filters the lines read from the log file
        @return None
        """
        try:
            self._filtered_logs = self._filtered_logs.split(SEPERATOR)
            self._filtered_logs = list(filter(lambda s: KEY in s and IS_CONFIG_RELATED not in s, self._filtered_logs))
        except ValueError: 
            print("Something went wrong when filtering the auditd log", file=stderr)
            exit(BAD_PARSE)

    def parse_actions(self) -> None:
        """
        This function creates the SQLModel Actions which are saved on the DB
        @return None
        """
        for log in self._filtered_logs:
            try:
                call_type = log.rsplit(SYSCALL_SEPARATOR, 1)[1]
                call_type = call_type[1:call_type.index(" ")]
                succeeded = log.split(SUCCESS_SEPARATOR, 1)[1]
                succeeded = succeeded[1:succeeded.index(" ")]
                succeeded = 1 if succeeded == "yes" else 0
                calling_user = resplit(USER_SEPARATOR, log)[1]
                calling_user = calling_user[2:calling_user.index('"', 2)]
            except ValueError:
                print("Something went wrong while parsing the filtered data", file=stderr)
                exit(BAD_PARSE)

            self._actions.append(Actions(syscall_type=call_type, calling_user=calling_user, success=succeeded))

    @property
    def actions(self) -> list[Actions]:
        return self._actions

