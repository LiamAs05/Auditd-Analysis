#! /usr/bin/python3

class AuditAnalyzer:
    def __init__(self):
        self._log_path = "/var/log/audit/audit.log"

    def read_logs(self) -> list[str]:
        with open(self._log_path, "r") as log_file:
            return log_file.readlines()

        
