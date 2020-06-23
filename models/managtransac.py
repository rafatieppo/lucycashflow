# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to manage transactions
# ======================================================================

class managtransac:
    def __init__(self, connection):
        self.connection = connection

    def find_byid(self, id_trans):
        connection = self.connection
        self.id_trans = id_trans
        with connection:
            cursor = connection.cursor()
            query = "SELECT * FROM transacao WHERE transacao_id=?"
            result = cursor.execute(query, (id_trans,))
            row = result.fetchone()
            if row is not None:
                return {'transacao': {'id': row[0], 'tipo': row[1], 'conta':row[3]}}
            else:
                return {'transacao': {'id': [-99], 'tipo': [-99], 'conta': [-99]}}
                print('Transacao ' + str(id_trans) + ' nao existe')

    def insert(self, tipo_id, data, conta_id, categoria_id,
               subcategoria_id, valor, obs):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            if tipo_id == 1:
                valor = valor * -1
            query = "INSERT INTO transacao VALUES (NULL, ?,?,?,?,?,?,?);"
            cursor.execute(query, (tipo_id, data, conta_id,
                                   categoria_id, subcategoria_id, valor, obs,))
            connection.commit()
        print('Transacao' + 'registrada com sucesso')

    def delete(self, id_trans, conta):
        contafound = self.find_byid(id_trans)
        print(contafound['transacao']['conta'])
        print('conta digitada é ', str(conta) + 'e conta encontrada é ' + str(contafound['transacao']['conta']))
        if str(contafound['transacao']['conta']) == str(conta):
            connection = self.connection
            with connection:
                cursor = connection.cursor()
                query = "DELETE FROM transacao WHERE transacao_id=?;"
                cursor.execute(query, (id_trans,))
                connection.commit()
            print('Transacao ' + str(id_trans) + ' excluida com sucesso')
        else:
            print('Transacao ' + str(id_trans) + ' nao existe ou não corresponde com a conta')
