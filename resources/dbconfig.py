# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to create configuracoes
# ======================================================================

import sqlite3

class config_db:
    def __init__(self, connection):
        # self.db_filename = db_filename
        self.connection = connection

    def config(self):
        with self.connection:
            cursor = self.connection.cursor()    
            cursor.execute('PRAGMA foreign_keys = ON')
            self.connection.commit()
