# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to manage transferences
# ======================================================================

import datetime as dt
import string
import random

class managtransf:
    def __init__(self, connection):
        self.connection = connection

    def find_byid(self, id_transf):
        connection = self.connection
        self.id_transf = id_transf
        with connection:
            cursor = connection.cursor()
            query = "SELECT * FROM transferencia WHERE transferencia_id=?"
            result = cursor.execute(query, (id_transf,))
            row = result.fetchone()
            if row is not None:
                return {'Transferencia': {'id': row[0], 'tipo_id': row[1], 'conta_id':row[3]}}
            else:
                print('Trans ' + str(id_transf) + ' nao existe')
                return {'Transferencia': {'id': [-99], 'tipo_id': [-99], 'conta_id':[-99]}}
                
    def insert(self, data, conta_id, to_conta_id, valor, obs):
        connection = self.connection
        valorneg = valor * -1
        rl = (random.choice(string.ascii_letters) +
              str(dt.datetime.now().year) +
              str(dt.datetime.now().month) +
              str(dt.datetime.now().day) +
              str(dt.datetime.now().hour) +
              str(dt.datetime.now().minute) +
              str(dt.datetime.now().second))
        with connection:
            cursor = connection.cursor()
            query = "INSERT INTO transferencia VALUES (NULL, 3, ?, ?, ?, NULL, NULL, ?, ?, ?);"
            cursor.execute(query,
                           (data, conta_id, to_conta_id, valorneg, obs, rl,))
            query = "INSERT INTO transferencia VALUES (NULL, 3, ?, ?, NULL, NULL, NULL, ?, ?, ?);"
            cursor.execute(query,
                           (data, to_conta_id, valor, str('oriundo conta ' + str(conta_id)), rl,))
            connection.commit()
            print('Transferencia da conta ' + str(conta_id) + ' para ' +
                  str(to_conta_id) + ' registrada com sucesso')

    def delete(self, id_transf, contat):
        contafoundt = self.find_byid(id_transf)
        # print(contafoundt['Transferencia']['conta_id'])
        # print('conta digitada é ', str(contat) + 'e conta encontrada é ' + str(contafoundt['transferencia']['conta_id']))
        if str(contafoundt['Transferencia']['conta_id']) == str(contat):
            connection = self.connection
            with connection:
                cursor = connection.cursor()
                # query = "DELETE FROM transferencia WHERE transferencia_id=?;"
                query = "SELECT * FROM transferencia WHERE transferencia_id=?;"
                result = cursor.execute(query, (id_transf,))
                row = result.fetchone()
                row = row[9]
                if row is not None:
                    query = "DELETE FROM transferencia WHERE transferencia_ownkey=?;"
                    cursor.execute(query, (row,))
                    connection.commit()
                else:
                    print('Trans ' + str(id_transf) + ' com ' + str(row) + ' nao existe')
            print('Transferencia ' + str(id_transf) + ' excluida com sucesso')
        else:
            print('Transferencia ' + str(id_transf) + ' nao existe ou nao corresponde com a conta')
