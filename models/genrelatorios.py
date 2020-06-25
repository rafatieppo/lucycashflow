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
            WHERE data >=?  AND data <=?
            UNION ALL
            SELECT conta_nome,  valor AS valor FROM transferencia
            INNER JOIN conta ON transferencia.conta_id=conta.conta_id
            WHERE data >=? AND data <=?)
            GROUP BY conta_nome;
            """
            result = cursor.execute(
                query, (self.di, self.df, self.di, self.df))
            row = result.fetchall()
            if row is not None:
                print('Extrato gerado com sucesso')
                return row
            else:
                print('Nao foi possivel gerar extrato')
