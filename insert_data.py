import sqlite3
import pandas as pd
import datetime as dt
import string
import random


# ------------------------------------------------------------
# CRIAR CONTAS
# ------------------------------------------------------------

connection = sqlite3.connect('db_lucycashflow.db')
cursor = connection.cursor()
cursor.execute('PRAGMA foreign_keys = ON')
connection.commit()


ls_conta = ['BB_CC', 'BB_CP', 'BB_INV', 'CEF_CC', 'CEF_CP', 'CRED_CARD',
            'MYCAP', 'SICREDI_CC', 'SICREDI_CP', 'SICREDI_APLIC', 'TESOURO']

ls_saldo = [100801.83, 12500, 0, 10753.56, 0, 0,
            13000, 0, 0, 0, 0]

cursor = connection.cursor()

for i in range(len(ls_conta)):
    query = "INSERT INTO conta VALUES (NULL, ?, ?);"
    cursor.execute(query, (ls_conta[i], ls_saldo[i],))

connection.commit()
connection.close()

# ------------------------------------------------------------
# TRANSACAO
# ------------------------------------------------------------

df = pd.read_excel('./new_db_money_from2016.xlsx',
                   sheet_name='INOUT_DONE')
df.info()

connection = sqlite3.connect('db_lucycashflow.db')

cursor = connection.cursor()
cursor.execute('PRAGMA foreign_keys = ON')
connection.commit()

# TRANSACAO
for i in range(len(df)):
    data = df.iloc[i, 0]
    tipoid = int(df.iloc[i, 13])
    contaid = int(df.iloc[i, 14])
    categid = int(df.iloc[i, 12])
    subcaid = int(df.iloc[i, 9])
    if df.iloc[i, 13] == 1:
        val = df.iloc[i, 15] * -1
    else:
        val = df.iloc[i, 15]
    obs = str(df.iloc[i, 2])
    query = "INSERT INTO transacao VALUES (NULL, ?,?,?,?,?,?,?);"
    cursor.execute(query, (tipoid, data, contaid, categid, subcaid, val,
                           obs,))

connection.commit()
connection.close()

# ------------------------------------------------------------
# TRANSFERENCIA
# ------------------------------------------------------------

df_trans = pd.read_excel('./new_db_money_from2016.xlsx',
                         sheet_name='TRANFS_DONE')

df_trans.info()
df_trans.head()

connection = sqlite3.connect('db_lucycashflow.db')
cursor = connection.cursor()
cursor.execute('PRAGMA foreign_keys = ON')
connection.commit()

for i in range(len(df_trans)):
    data = df_trans.iloc[i, 0]
    fromid = int(df_trans.iloc[i, 7])
    toid = int(df_trans.iloc[i, 8])
    valor = df_trans.iloc[i, 9]
    valorneg = valor * -1
    obs = "xxx"
    rl = (random.choice(string.ascii_letters) +
          str(dt.datetime.now().year) +
          str(dt.datetime.now().month) +
          str(dt.datetime.now().day) +
          str(dt.datetime.now().hour) +
          str(dt.datetime.now().minute) +
          str(dt.datetime.now().second))
    cursor = connection.cursor()
    query = "INSERT INTO transferencia VALUES (NULL, 3, ?, ?, ?, NULL, NULL, ?, ?, ?);"
    cursor.execute(query,
                   (data, fromid, toid, valorneg, obs, rl,))
    query = "INSERT INTO transferencia VALUES (NULL, 3, ?, ?, ?, NULL, NULL, ?, ?, ?);"
    cursor.execute(query,
                   (data, toid, fromid, valor, str('oriundo conta ' + str(fromid)), rl,))

connection.commit()
connection.close()


# ------------------------------------------------------------
# ------------------------------------------------------------
