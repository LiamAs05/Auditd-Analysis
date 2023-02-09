
# Auditd Logs Analyzer

Created as an home assignment for the Magshimim + Cyngular Security job offer. This program will focus on analyzing syscalls by defining system call rules.

System call rules are added to auditd using this syntax:
`auditctl -a action,filter -S system_call -F field=value -k key_name`
## Rule Setup

We will add the following auditd rule: `sudo auditctl -a always,exit -F arch=b64 -S fork`

A deeper understading of the command:

`"-F arch=b-64" specifies that the rule is targeted for 64-bit system`

`"-S fork" specifies the rule targets "fork" syscall`

`"-a always" tells the auditd daemon to always log the syscalls`

`"exit" check if audit event needs to be created upon syscall exit`
## Code Walkthorugh

The `AuditAnalyzer` class is where the analysis happens. It has one attribute which is a constant and specifies the path of the audit log file.
```py
class AuditAnalyzer:
    def __init__(self):
        self._log_path = "/var/log/audit/audit.log"
```

The `read_logs` function reads the lines inside the audit log file and returns a list containing them.
```py
    def read_logs(self) -> list[str]:
        with open(self._log_path, "r") as log_file:
            return log_file.readlines()

```