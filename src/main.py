#! /usr/bin/python3

from Visualizer import Visualizer
from AuditAnalyzer import AuditAnalyzer
from DBManager import DBManager
from sys import stderr
from os import _exit
from time import sleep
INTERRUPT = -2

def main():
    analyzer = AuditAnalyzer()
    db = DBManager()
    db.add_actions(analyzer.actions)
    
    status_dict = db.get_status()
    syscalls_list = db.get_syscalls()
    users_dict = db.get_users()

    print(f"There were {status_dict[1]} system calls that succeeded and {status_dict[0]} that failed.")
    sleep(1)
    print(f"The user that made the most syscalls was {max(users_dict, key=users_dict.get)}.")
    sleep(1)
    print(f"The distribution of the calls is showed in the following graph...")
    sleep(2)
    Visualizer.visualize(db.get_syscalls())

if __name__ == "__main__":
    try:
        main() 
    except KeyboardInterrupt as e:
        print("Ctrl+C pressed, exiting...", file=stderr)
        try:
            exit(INTERRUPT)
        except SystemExit:
            _exit(INTERRUPT)
