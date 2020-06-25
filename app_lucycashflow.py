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
from flask import request, flash
# url_for, redirect


from flask_bootstrap import Bootstrap
import os


# connecting
cdb = connect_db('db_lucycashflow.db')

app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():
    connection = cdb.fconnecta()
    conf = config_db(connection)
    conf.config()
    # get bank statement from db
    if request.method == "POST" and request.form['action'] == 'GerarRelatorio':
        di = request.form.get('datai', False)
        df = request.form.get('dataf', False)
        connection = cdb.fconnecta()
        conf = config_db(connection)
        conf.config()
        reports_all = genrelatorios(connection, di, df)
        bal_allacc = reports_all.balance_allacc()
        if bal_allacc[0][1] is None:
            flash(' - Não há transações entre  ** ' + di + ' ** e ** ' + df +
                  '**')
        else:
            flash(' - Relatório de ** ' + di + ' ** a ** ' + df +
                  '** gerado com sucesso ', 'info')
        return render_template('relatorio.html',
                               bal_allacc=bal_allacc)
    else:
        return render_template('relatorio.html')


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
