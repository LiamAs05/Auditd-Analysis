#! /usr/bin/python3

from AuditAnalyzer import AuditAnalyzer
from DBManager import DBManager
from sys import stderr
from os import _exit

INTERRUPT = -2

def main():
    analyzer = AuditAnalyzer()
    db = DBManager()
    db.add_actions(analyzer.actions)

if __name__ == "__main__":
    try:
        main() 
    except KeyboardInterrupt as e:
        print("Ctrl+C pressed, exiting...", file=stderr)
        try:
            exit(INTERRUPT)
        except SystemExit:
            _exit(INTERRUPT)
