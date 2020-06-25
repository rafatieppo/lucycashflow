# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to create extrato
# ======================================================================


class genextratos:
    def __init__(self, connection, nome, di, df):
        self.connection = connection
        self.nome = nome
        self.di = di
        self.df = df

    def ext_bycount(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
                SELECT transacao.transacao_id AS ID, transacao.data, tipo.tipo_nome,
                conta.conta_nome, categoria.categoria_nome AS categoria,
                subcategoria.subcategoria_nome AS subcategoria, valor, obs
                FROM transacao
                INNER JOIN categoria ON transacao.categoria_id=categoria.categoria_id
                INNER JOIN subcategoria ON transacao.subcategoria_id=subcategoria.subcategoria_id
                INNER JOIN conta ON transacao.conta_id=conta.conta_id
                INNER JOIN tipo ON transacao.tipo_id=tipo.tipo_id
                WHERE conta.conta_id=? AND data >=? AND data <=?
                UNION ALL 
                SELECT transferencia.transferencia_id AS ID, transferencia.data,
                tipo.tipo_nome, conta.conta_nome,
                transferencia.categoria_id AS categoria,
                transferencia.subcategoria_id AS subcategoria,
                valor, obs
                FROM transferencia
                INNER JOIN conta ON transferencia.conta_id=conta.conta_id
                INNER JOIN tipo ON transferencia.tipo_id=tipo.tipo_id 
                WHERE conta.conta_id=? AND data >=? AND data <=?;
                """
            result = cursor.execute(
                query, (self.nome, self.di, self.df, self.nome, self.di, self.df))
            row = result.fetchall()
            if row is not None:
                print('Extrato gerado com sucesso')
                return row
            else:
                print('Nao foi possivel gerar extrato')

    def saldo_bycount(self):
        connection = self.connection
        with connection:
            cursor = connection.cursor()
            query = """
            SELECT ID, SUM(valor) FROM (
            SELECT 1 as ID, SUM(valor) AS valor FROM transacao
            WHERE transacao.conta_id=? AND data >=? AND data <=?
            UNION ALL
            SELECT 1 as ID,  SUM(valor) AS valor FROM transferencia
            WHERE transferencia.conta_id=? AND data >=? AND data <=?);
            """
            result = cursor.execute(
                query, (self.nome, self.di, self.df, self.nome, self.di, self.df))
            row = result.fetchall()
            if row is not None:
                print('Saldo gerado com sucesso')
                return row
            else:
                print('Nao foi possivel gerar saldo')
