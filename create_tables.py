# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to create and fill  tables
# ======================================================================

import sqlite3
import re


class connect_db:
    def __init__(self, db_filename):
        self.db_filename = db_filename

    def fconnecta(self):
        return sqlite3.connect(self.db_filename)
    # connection = sqlite3.connect(db_filename)


class make_tables:
    def __init__(self, connection):
        self.connection = connection

    # decorator to check if table exists
    def dchecktable(func):
        def fconnect(self, *args, **kargs):
            connection = self.connection
            with connection:
                cursor = connection.cursor()
                create_table = func()
                cursor.execute(create_table)
                connection.commit()
                ttt = re.search('EXISTS(.*)\(', create_table)
                if ttt is None:
                    ttt = '---'
                else:
                    ttt = ttt.group(1)
                print('Table \n' + ttt + ' \n was created \n \n')
        return fconnect

    # table tipo
    @dchecktable
    def ftb_tipo():
        create_table = """
        CREATE TABLE IF NOT EXISTS tipo (tipo_id INTEGER PRIMARY KEY,
        tipo_nome text NOT NULL)"""
        return create_table

    # table conta banco1 banco2 ... bancon
    @dchecktable
    def ftb_conta():
        create_table = """
        CREATE TABLE IF NOT EXISTS conta (conta_id
        INTEGER PRIMARY KEY,
        conta_nome text NOT NULL UNIQUE,
        conta_saldo DECIMAL NOT NULL)"""
        return create_table

    # table categoria
    @dchecktable
    def ftb_categoria():
        create_table = """
        CREATE TABLE IF NOT EXISTS categoria (categoria_id INTEGER PRIMARY KEY,
        tipo_id INTEGER NOT NULL REFERENCES tipo(tipo_id),
        categoria_nome text NOT NULL)"""
        return create_table

    # table subcategoria
    @dchecktable
    def ftb_subcategoria():
        create_table = """
        CREATE TABLE IF NOT EXISTS subcategoria (subcategoria_id INTEGER
        PRIMARY KEY,
        categoria_id INTEGER NOT NULL REFERENCES categoria(categoria_id),
        subcategoria_nome text NOT NULL)"""
        return create_table

    # table transacao
    @dchecktable
    def ftb_transacao():
        create_table = """
        CREATE TABLE IF NOT EXISTS transacao (transacao_id INTEGER PRIMARY KEY,
        tipo_id INTEGER NOT NULL REFERENCES tipo(tipo_id),
        data TEXT NOT NULL,
        conta_id INTEGER NOT NULL REFERENCES conta(conta_id),
        categoria_id INTEGER NOT NULL REFERENCES categoria(categoria_id),
        subcategoria_id INTEGER NOT NULL REFERENCES subcategoria(subcategoria_id),
        valor DECIMAL NOT NULL, obs TEXT)"""
        return create_table

    # table transferencia
    @dchecktable
    def ftb_transferencia():
        create_table = """
        CREATE TABLE IF NOT EXISTS transferencia
        (transferencia_id INTEGER PRIMARY KEY,
        tipo_id INTEGER NOT NULL REFERENCES tipo(tipo_id),
        data TEXT NOT NULL,
        conta_id INTEGER NOT NULL REFERENCES conta(conta_id),
        to_conta_id INTEGER NOT NULL REFERENCES conta(conta_id),
        categoria_id INTEGER,
        subcategoria_id INTEGER,
        valor DECIMAL NOT NULL,
        obs TEXT,
        transferencia_ownkey TEXT)"""
        return create_table


class populate_tables:
    def __init__(self, connection):
        self.connection = connection

    def fpop_conta(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = "SELECT * FROM conta;"
            result = cursor.execute(query)
            row = result.fetchall()
            if len(row) > 0:
                print("\n Tabela conta preenchida \n")
            else:
                ls_fill = ['MinhaCarteira']
                ls_filla = [0]
                for i in range(len(ls_fill)):
                    ins = str("INSERT INTO conta VALUES (NULL, '" +
                              str(ls_fill[i]) + "', " + str(ls_filla[i]) + ")")
                    cursor.execute(ins)
                connection.commit()

    def fpop_tipo(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = "SELECT * FROM tipo;"
            result = cursor.execute(query)
            row = result.fetchall()
            if len(row) > 0:
                print("\n Tabela tipo preenchida \n")
            else:
                ls_fill = ['despesa', 'receita', 'transferencia']
                for i in ls_fill:
                    ins = str("INSERT INTO tipo VALUES (NULL, '" + i + "')")
                    cursor.execute(ins)
                connection.commit()

    def fpop_categoria(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = "SELECT * FROM categoria;"
            result = cursor.execute(query)
            row = result.fetchall()
            if len(row) > 0:
                print("\n Tabela categoria preenchida \n")
            else:
                ls_fill = ['imposto', 'moradia', 'outras_despesas',
                           'outras_receitas', 'pessoal', 'salario',
                           'tx_bancaria', 'veiculo', 'viagem']
                ls_fk = [1, 1, 1, 2, 1, 2, 1, 1, 1]
                for i in range(len(ls_fill)):
                    ins = str("INSERT INTO categoria VALUES (NULL, '" +
                              str(ls_fk[i]) + "', "+"'" + ls_fill[i] + "')")
                    cursor.execute(ins)
                connection.commit()

    def fpop_subcategoria(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = "SELECT * FROM subcategoria;"
            result = cursor.execute(query)
            row = result.fetchall()
            if len(row) > 0:
                print("\n Tabela subcategoria preenchida \n")
            else:
                ls_fill = ['documentos', 'iptu', 'ipva', 'ir',
                           'agua', 'aluguel', 'diarista', 'eletro_eletron', 'energia',
                           'interior', 'internet', 'manutencao', 'mercado', 'prestacao', 'telefonia',
                           'bike', 'computador', 'doacoes', 'eletronico', 'emprestimo', 'geral', 'pet', 'presente',
                           'aplicacao', 'bolsa', 'devolucao_emprestimo', 'devolucao_imposto', 'diversos', 'locacao',
                           'alimentacao', 'calcado', 'celular', 'educacao', 'hig_saude', 'lazer',
                           'livrorevista', 'vestuario', 'trabalho',
                           'job01', 'job02', 'job03',
                           'anuidade', 'juro',
                           'aquisicao', 'combustivel', 'mecanica', 'seguro',
                           'estadia', 'refeicao', 'transporte']
                ls_fk = [1, 1, 1, 1,
                         2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                         3, 3, 3, 3, 3, 3, 3, 3,
                         4, 4, 4, 4, 4, 4,
                         5, 5, 5, 5, 5, 5, 5, 5, 5,
                         6, 6, 6,
                         7, 7,
                         8, 8, 8, 8,
                         9, 9, 9]
                for i in range(len(ls_fill)):
                    ins = str("INSERT INTO subcategoria VALUES (NULL, " +
                              str(ls_fk[i]) + ",'" + ls_fill[i] + "')")
                    cursor.execute(ins)
                connection.commit()

# ------------------------------------------------------------
# import numpy as np
#
# fk =[np.repeat(1,3),
# np.repeat(2,3),
# np.repeat(3,2),
# np.repeat(4,8),
# np.repeat(5,5),
# np.repeat(6,9),
# np.repeat(7,3),
# np.repeat(8,5),
# np.repeat(9,3)]
# fk = list(np.concatenate(fk))
# fk
#
