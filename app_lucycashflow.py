# ======================================================================
#                                         https://rafatieppo.github.io/
#                                         13-06-2020
# file to create the app
# ======================================================================

from resources.connex import connect_db
from resources.dbconfig import config_db
from models.managacount import managacount
from models.managtransac import managtransac
from models.managtransf import managtransf
from models.genextratos import genextratos
from models.genrelatorios import genrelatorios
from flask import Flask
from flask import render_template
from flask import request, flash, jsonify
# url_for, redirect
# from flask_bootstrap import Bootstrap
import os
import pandas as pd
import json
import datetime as dt
import numpy as np

# connecting
cdb = connect_db('db_lucycashflow.db')

app = Flask(__name__)
# Bootstrap(app)

app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/relatorio_categ", methods=["GET", "POST"])
def relatorio_categ():
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    di = request.form.get('datai', False)
    df = request.form.get('dataf', False)
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    reports_all = genrelatorios(connection, di, df)
    # bal_overall = reports_all.report_categories()
    # ------------------------------------------------------------
    # labels = ["January", "February", "March",
    #           "April", "May", "June", "July", "August"]
    # values = [10, 9, 8, 7, 6, 4, 7, 8]
    # ------------------------------------------------------------
    # input output balance by month
    if request.method == "POST" and request.form['action'] == 'GerarRelatorio':
        # balance for accounts
        outmonthcateg = reports_all.report_categories()
        ls_dt = []
        ls_ct = []
        ls_vl = []
        for i in range(len(outmonthcateg)):
            ls_dt.append(outmonthcateg[i][0])
            ls_ct.append(outmonthcateg[i][1])
            ls_vl.append(outmonthcateg[i][2])
        df_outmonthcateg = pd.DataFrame({'data': ls_dt,
                                         'catt': ls_ct,
                                         'valor': ls_vl})
        # js plot
        maxx = max(ls_vl) * 1.1
        xx = df_outmonthcateg.pivot_table(index='data',
                                          values='valor',
                                          columns='catt',
                                          fill_value=0)
        labels = list(xx.index)
        try:
            imposto = list(map(abs, xx['imposto']))
        except KeyError:
            imposto = list(np.repeat(0, len(xx)))
        try:
            moradia = list(map(abs, xx['moradia']))
        except KeyError:
            moradia = list(np.repeat(0, len(xx)))
        try:
            outras_despesas = list(map(abs, xx['outras_despesas']))
        except KeyError:
            outras_despesas = list(np.repeat(0, len(xx)))
        try:
            pessoal = list(map(abs, xx['pessoal']))
        except KeyError:
            pessoal = list(np.repeat(0, len(xx)))
        try:
            tx_bancaria = list(map(abs, xx['tx_bancaria']))
        except KeyError:
            tx_bancaria = list(np.repeat(0, len(xx)))
        try:
            veiculo = list(map(abs, xx['veiculo']))
        except KeyError:
            veiculo = list(np.repeat(0, len(xx)))
        try:
            viagem = list(map(abs, xx['viagem']))
        except KeyError:
            viagem = list(np.repeat(0, len(xx)))
        if outmonthcateg is None:
            flash(' - Não há transações entre  ** ' + di + ' ** e ** ' + df +
                  '**')
        else:
            flash(' - Relatório de ** ' + di + ' ** a ** ' + df +
                  '** ', 'info')
        return render_template('relatorio_categ.html',
                               outmonthcateg=outmonthcateg,
                               df_outmonthcateg=df_outmonthcateg,
                               labels=labels, imposto=imposto,
                               moradia=moradia,
                               outras_despesas=outras_despesas,
                               pessoal=pessoal,
                               tx_bancaria=tx_bancaria, veiculo=veiculo,
                               viagem=viagem)
    else:
        return render_template('relatorio_categ.html')

# ------------------------------------------------------------


@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    di = request.form.get('datai', False)
    df = request.form.get('dataf', False)
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    reports_all = genrelatorios(connection, di, df)
    bal_overall = reports_all.balance_overall()
    bal_allacc = reports_all.balance_allacc()
    # ------------------------------------------------------------
    # labels = ["January", "February", "March",
    #           "April", "May", "June", "July", "August"]
    # values = [10, 9, 8, 7, 6, 4, 7, 8]
    # ------------------------------------------------------------
    # input output balance by month
    if request.method == "POST" and request.form['action'] == 'GerarRelatorio':
        # balance for accounts
        inoutbalmonth = reports_all.inout_month()
        ls_dt = []
        ls_ty = []
        ls_vl = []
        for i in range(len(inoutbalmonth)):
            ls_dt.append(inoutbalmonth[i][0])
            ls_ty.append(inoutbalmonth[i][1])
            ls_vl.append(inoutbalmonth[i][2])
        df_inoutbalmonth = pd.DataFrame({'data': ls_dt,
                                         'tipo': ls_ty,
                                         'valor': ls_vl})
        df_inoutbalmonth = df_inoutbalmonth.query(
            'tipo != "saldo"').reset_index()
        # js plot
        maxx = max(ls_vl) * 1.1
        xx = df_inoutbalmonth.pivot_table(index='data',
                                          values='valor',
                                          columns='tipo',
                                          fill_value=0)
        labels = list(xx.index)
        despesas = list(map(abs, xx['despesa']))
        receitas = list(map(abs, xx['receita']))

        # report by categoria
        expense_categ = reports_all.expenses_categories()
        # report by categoria
        expense_subcateg = reports_all.expenses_subcategories()

        if inoutbalmonth is None:
            flash(' - Não há transações entre  ** ' + di + ' ** e ** ' + df +
                  '**')
        else:
            flash(' - Relatório de ** ' + di + ' ** a ** ' + df +
                  '** ', 'info')
        return render_template('relatorio.html',
                               bal_allacc=bal_allacc,
                               bal_overall=bal_overall,
                               inoutbalmonth=inoutbalmonth,
                               df_inoutbalmonth=df_inoutbalmonth,
                               labels=labels, despesas=despesas,
                               receitas=receitas,
                               expense_categ=expense_categ,
                               expense_subcateg=expense_subcateg)
    # max=maxx, values=values,
    # ls_fillcolor=ls_fillcolor)
    else:
        return render_template('relatorio.html',
                               bal_allacc=bal_allacc,
                               bal_overall=bal_overall)
        # inoutbalmonth=inoutbalmonth,
        # df_inoutbalmonth=df_inoutbalmonth,
        # labels=labels, max=maxx, values=values,
        # ls_fillcolor=ls_fillcolor,
        # despesas=despesas, receitas=receitas)


@app.route("/extrato", methods=["GET", "POST"])
def extrato():
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM conta ORDER BY conta.conta_nome;")
    contas = result.fetchall()
    # test if value was passed in (e.g. GET method), default value is 1
    selected = request.args.get('choice_categ', '1')
    # application 'state' variable with default value and test
    state_categ = {'choice_categ': selected}
    # get bank statement from db
    if request.method == "POST" and request.form['action'] == 'GerarExtrato':
        di = request.form.get('datai', False)
        df = request.form.get('dataf', False)
        cc = request.form.get('conta', False)
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        statem_count = genextratos(connection, cc, di, df)
        statem = statem_count.ext_bycount()
        balance = statem_count.saldo_bycount()
        if balance[0][1] is not None:
            balance = str(float(balance[0][1]))
        else:
            balance = ''
        flash(' - Extrato de ** ' + di + ' ** a ** ' + df +
              '**  -------> SALDO: $ ' + balance, 'info')
        return render_template('extrato.html',
                               contas=contas,
                               state_categ=state_categ,
                               statem=statem,
                               balance=balance)
    else:
        return render_template('extrato.html',
                               contas=contas,
                               state_categ=state_categ)


@app.route("/gerenciartransac", methods=["GET", "POST"])
def gerenciartransac():
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM conta")
    contas = result.fetchall()
    # test if value was passed in (e.g. GET method), default value is 1
    selected = request.args.get('choice_categ', '1')
    # application 'state' variable with default value and test
    state_categ = {'choice_categ': selected}
    if request.method == "POST" and request.form['action'] == 'ExcluirTransacao':
        iid = request.form.get('idd', False)
        conta = request.form.get('conta', False)
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        managtrans = managtransac(connection)
        managtrans.delete(iid, conta)

    if request.method == "POST" and request.form['action'] == 'ExcluirTransferencia':
        iidf = request.form.get('iddt', False)
        conta = request.form.get('contat', False)
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        managtransff = managtransf(connection)
        managtransff.delete(iidf, conta)

    return render_template('gerenciartransac.html',
                           contas=contas,
                           state_categ=state_categ)


@app.route("/transferencias", methods=["GET", "POST"])
def transferencias():
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM conta ORDER BY conta.conta_nome;")
    contas = result.fetchall()
    # test if value was passed in (e.g. GET method), default value is 1
    selected = request.args.get('choice_categ', '1')
    # application 'state' variable with default value and test
    state_categ = {'choice_categ': selected}
    if request.method == "POST" and request.form['action'] == 'Transferir':
        dataa = request.form.get('data', False)
        fromcont = request.form.get('deconta', False)
        tocont = request.form.get('paraconta', False)
        valoo = request.form.get('valor', False)
        obsss = request.form.get('obs', False)
        print('------------------------------------------------------------')
        # print(tipoo)
        # print(obsss)
        # print(valoo)
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        managtransff = managtransf(connection)
        managtransff.insert(dataa, fromcont, tocont, float(valoo), obsss)
    return render_template('transferencias.html',
                           contas=contas,
                           state_categ=state_categ)


@app.route("/lancamentos", methods=["GET", "POST"])
def lancamentos():
    # list of tuples representing select options
    # categorias = [(str(x), str(x)) for x in range(1, 20)]
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    cursor = connection.cursor()
    # get info for dropdown
    result = cursor.execute("SELECT * FROM conta ORDER BY conta.conta_nome;")
    contas = result.fetchall()
    result = cursor.execute('SELECT * FROM tipo WHERE tipo.tipo_id <> 3')
    tipos = result.fetchall()
    result = cursor.execute("""
        SELECT categoria.categoria_id, categoria.categoria_nome,
        tipo.tipo_nome
        FROM categoria
        INNER JOIN tipo ON tipo.tipo_id=categoria.tipo_id
        ORDER BY tipo.tipo_nome DESC;
        """)
    categorias = result.fetchall()
    ls_categorias = []
    for i in range(len(categorias)):
        a = categorias[i][0]
        b = categorias[i][1]
        c = categorias[i][2]
        f = str(c + " : " + b)
        t = (a, f)
        ls_categorias.append(t)
    categorias = ls_categorias
    result = cursor.execute("""
        SELECT subcategoria.subcategoria_id, subcategoria.subcategoria_nome,
        categoria.categoria_nome
        FROM subcategoria
        INNER JOIN categoria ON categoria.categoria_id=subcategoria.categoria_id;
        """)
    subs = result.fetchall()
    ls_subtuple = []
    for i in range(len(subs)):
        a = subs[i][0]  # sub id
        b = subs[i][1]  # sub nome
        c = subs[i][2]  # categ
        f = str(c + " : " + b)
        t = (a, f)
        ls_subtuple.append(t)
    subs = ls_subtuple
    # test if value was passed in (e.g. GET method), default value is 1
    selected = request.args.get('choice_categ', '1')
    # application 'state' variable with default value and test
    state_categ = {'choice_categ': selected}
    if request.method == "POST" and request.form['action'] == 'Lancar':
        # fff = request.form.get('valor', False)
        # fff = request.form.to_dict(False)
        tipoo = request.form.get('tipo', False)
        dataa = request.form.get('data', False)
        contt = request.form.get('conta', False)
        catee = request.form.get('categoria', False)
        subss = request.form.get('subs', False)
        valoo = request.form.get('valor', False)
        # if int(tipoo) == 1:
        #     valoo = valoo * -1
        obsss = request.form.get('obs', False)
        # tipoo = fff['tipo']
        # dataa = fff['data']
        # contt = fff['conta']
        # catee = fff['categoria']
        # subss = fff['subs']
        # valoo = fff['valor']
        # obsss = fff['obs']
        # valoo= float(valoo)
        # valoo = valoo
        # tipoo = (int(tipoo[0]))
        # valoo = (float(valoo[0]))
        # print('------------------------------------------------------------')
        if tipoo == '1':
            valoo = float(valoo) * -1
        else:
            valoo = float(valoo)
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        managtrans = managtransac(connection)
        managtrans.insert(tipoo, dataa, contt, catee, subss, valoo, obsss)
    return render_template('lancamentos.html',
                           tipos=tipos,
                           contas=contas,
                           categorias=categorias,
                           subs=subs,
                           state_categ=state_categ)


@app.route("/gerenciarconta", methods=["GET", "POST"])
def gerconta():
    if request.method == "POST" and request.form['action'] == 'Cadastrar':
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        managconta = managacount(connection)
        form = request.form
        nome = form['nome']
        saldo = form['saldo']
        managconta.insert(nome, float(saldo))
        flash('Conta inserida com sucesso', 'success')
    elif request.method == "POST" and request.form['action'] == 'Excluir':
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        managconta = managacount(connection)
        form = request.form
        nome = form['nome2']
        managconta.delete(nome)
        flash('Conta excluída com sucesso', 'danger')
    return render_template('gerenciarconta.html')


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# # connecting
# cdb = connect_db('db_lucycashflow.db')
# connection = cdb.fconnecta()

# # config sqlite3
# conf = config_db(connection)
# conf.config()

# # management
# managconta = managacount(connection)
# managtransac = managtransac(connection)
# managtransf = managtransf(connection)

# # ------------------------------------------------------------
# # find conta
# managconta.find_byname('conta0s44')
# # insert conta
# managconta.insert('conta045', 0)
# # delete conta
# managconta.delete('conta044')
# # update conta nome
# managconta.update('conta045', 'conta051')

# # ------------------------------------------------------------
# # find transacao
# managtransac.find_byid(2)
# # insert transacao
# managtransac.insert(1, '2020-06-22', 3, 1, 1, 5000, '')
# # delete transacao
# managtransac.delete(7)

# # ------------------------------------------------------------
# # find transferencia
# managtransf.find_byid(3)
# # insert transferencia
# managtransf.insert('2020-06-14', 1, 3, 111, '')
# # delete transferencia
# managtransf.delete(33)

# # ------------------------------------------------------------
