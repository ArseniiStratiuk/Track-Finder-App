# -*- coding: utf-8 -*-
import sqlite3
import os
import sys


class DbChinook:
    def __init__(self):
        self.connection = sqlite3.connect(os.path.join(sys.path[0], 'chinook.db'))
        self.cursor = self.connection.cursor()

    def select(self, query, *args):
        if args:
            self.cursor.execute(query, args)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()


if __name__ == '__main__':
    db = DbChinook()