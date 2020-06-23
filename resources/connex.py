# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
#  create connection with databank
# ======================================================================

import sqlite3

class connect_db:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def fconnecta(self):
        return sqlite3.connect(self.db_filename)
        # connection = sqlite3.connect(db_filename)
