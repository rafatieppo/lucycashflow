import sqlite3
from resources.connex import connect_db
from resources.dbconfig import config_db
from create_tables import make_tables
from create_tables import populate_tables

# connecting
cdb = connect_db('db_lucycashflow.db')
connection = cdb.fconnecta()

# config
conf = config_db(connection)
conf.config()

# creating tables
mt = make_tables(connection)
mt.ftb_tipo()
mt.ftb_conta()
mt.ftb_categoria()
mt.ftb_subcategoria()
mt.ftb_transacao()
mt.ftb_transferencia()

# filling tables
pt = populate_tables(connection)
pt.fpop_tipo()
pt.fpop_conta()
pt.fpop_categoria()
pt.fpop_subcategoria()
connection.close()
