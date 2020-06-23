# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to manage account
# ======================================================================

class managacount:
    def __init__(self, connection):
        self.connection = connection

    def find_byname(self, nome):
        connection = self.connection
        self.nome = nome
        with connection:
            # nome = 'conta01'
            cursor = connection.cursor()
            query = "SELECT * FROM conta WHERE conta_nome=?"
            result = cursor.execute(query, (nome,))
            row = result.fetchone()
            if row is not None:
                print('Conta ' + nome + ' EXISTENTE')
                return {'conta': {'conta_id': row[0], 'conta_nome': row[1]}}
            else:
                print('Conta ' + nome + ' nao existe')

    def insert(self, nome, saldo):
        conta = self.find_byname(nome)
        if conta is None:
            connection = self.connection
            with connection:
                cursor = connection.cursor()
                query = "INSERT INTO conta VALUES (NULL, ?, ?);"
                cursor.execute(query, (nome, saldo,))
                connection.commit()
            print('Conta ' + nome + ' registrada com sucesso')
        else:
            print('Conta ' + nome + ' NAO registrada')

    def delete(self, nome):
        conta = self.find_byname(nome)
        if conta is not None:
            connection = self.connection
            with connection:
                cursor = connection.cursor()
                query = "DELETE FROM conta WHERE conta_nome=?;"
                cursor.execute(query, (nome,))
                connection.commit()
            print('Conta ' + nome + ' excluida com sucesso')
        else:
            print('Conta ' + nome + ' nao existe')

    def update(self, nome, novonome):
        conta = self.find_byname(nome)
        if conta is not None:
            connection = self.connection
            with connection:
                cursor = connection.cursor()
                query = "UPDATE conta SET conta_nome=? WHERE conta_nome=?;"
                cursor.execute(query, (novonome, nome,))
                connection.commit()
            print('Conta ' + nome + ' atualizada com sucesso')
        else:
            print('Conta ' + nome + ' nao existe')
