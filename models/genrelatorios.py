# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to create extrato
# ======================================================================


class genrelatorios:
    def __init__(self, connection, di, df):
        self.connection = connection
        self.di = di
        self.df = df

    def balance_allacc(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
            SELECT conta_nome, sum(valor)
            FROM (
            SELECT conta_nome , valor AS valor FROM transacao
            INNER JOIN conta ON  transacao.conta_id=conta.conta_id
            UNION ALL
            SELECT conta_nome,  valor AS valor FROM transferencia
            INNER JOIN conta ON transferencia.conta_id=conta.conta_id
            )
            GROUP BY conta_nome;
            """
            result = cursor.execute(
                query)
            row = result.fetchall()
            if row is not None:
                print('Extrato gerado com sucesso')
                return row
            else:
                print('Nao foi possivel gerar extrato')

    def balance_overall(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
            SELECT sum(valor)
            FROM (
            SELECT conta_nome , valor AS valor FROM transacao
            INNER JOIN conta ON  transacao.conta_id=conta.conta_id
            UNION ALL
            SELECT conta_nome,  valor AS valor FROM transferencia
            INNER JOIN conta ON transferencia.conta_id=conta.conta_id) ;
            """
            result = cursor.execute(
                query)
            row = result.fetchall()
            if row is not None:
                print('Saldo geral gerado com sucesso')
                return row
            else:
                print('Nao foi possivel saldo geral')

    def inout_month(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
            SELECT transacao.data AS data, tipo.tipo_nome AS tipo, SUM(valor)
            FROM transacao
            INNER JOIN tipo ON transacao.tipo_id=tipo.tipo_id
            WHERE data >=? AND data <=?
            GROUP BY tipo, strftime("%m-%Y", data)
            UNION ALL
            SELECT data, tipo, SUM(valor)
            FROM (
            SELECT 'saldo' as tipo, data, tipo_id, valor FROM transacao)
            WHERE data >=? AND data <=?
            GROUP BY strftime("%m-%Y", data)
            ORDER BY data ASC;
            """
            result = cursor.execute(
                query, (self.di, self.df, self.di, self.df,))
            row = result.fetchall()
            if row is not None:
                print('Entradas, saidas e saldo mensal gerado com sucesso')
                return row
            else:
                print('Nao ha dados para o periodo')

    def expenses_categories(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
            SELECT categoria.categoria_nome AS categoria, SUM(valor)
            FROM transacao
            INNER JOIN categoria ON transacao.categoria_id=categoria.categoria_id
            WHERE data >=? AND data <=? AND transacao.tipo_id <> 2
            GROUP BY categoria;
            """
            result = cursor.execute(
                query, (self.di, self.df,))
            row = result.fetchall()
            if row is not None:
                print('Relatorio por categorias gerado com sucesso')
                return row
            else:
                print('Nao ha dados para o periodo')

    def expenses_subcategories(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
            SELECT categoria.categoria_nome AS categoria, subcategoria.subcategoria_nome AS subcategoria, SUM(valor)
            FROM transacao
            INNER JOIN categoria ON transacao.categoria_id=categoria.categoria_id
            INNER JOIN subcategoria ON transacao.subcategoria_id=subcategoria.subcategoria_id
            WHERE data >=? AND data <=? AND transacao.tipo_id <> 2
            GROUP BY subcategoria;
            """
            result = cursor.execute(
                query, (self.di, self.df,))
            row = result.fetchall()
            if row is not None:
                print('Relatorio por SUBcategorias gerado com sucesso')
                return row
            else:
                print('Nao ha dados para o periodo')
