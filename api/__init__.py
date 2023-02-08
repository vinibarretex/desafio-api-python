from flask import Flask, Blueprint, request, jsonify
from datetime import datetime, timedelta

from api.views import health

despesas = []

def create_app():
    app = Flask(__name__)

    # api é o nome (variável) do Blueprint, é usado pelo mecanismo de roteamento do Flask
    # __name__ é o nome de importação do Blueprint, que Flask usa para localizar os recursos do Blueprint.
    despesas_api = Blueprint('api', __name__)


    # define api routes
    despesas_api.add_url_rule('/status', 'health', view_func=health, methods=['GET'])


    # POST - Cadastrar despesa
    @despesas_api.route("/despesas", methods=["POST"])
    def cadastrar_despesa():
        dados = request.get_json() # armazenando as entradas do json na variável dados
        despesa = {
            "id": dados["id"],
            "valor": dados["valor"],
            "descricao": dados["descricao"],
            "data": dados["data"],
            "tipo_pagamento": dados["tipo_pagamento"],
            "categoria": dados["categoria"]
        }
        despesas.append(despesa)# adicionando a despesa inserida na lista despesas

        success = True if despesa in despesas else False
        # retorna True caso exista alguma despesa na lista 'despesas',
        # False caso contrario

        responseBody = {
            'success': success,
            'data': {"id": dados["id"]} # aqui é exibido o id da despesa adicionada
        }
        return jsonify(responseBody)

    # GET - Listar despesas
    @despesas_api.route("/despesas", methods=["GET"])
    def listar_despesas():
        hoje = datetime.now() # armazena a data e hora atual do sistema
        primeiro_dia_do_mes = hoje.replace(day=1) # representa o início do mês vigente
        ultimo_dia_do_mes = primeiro_dia_do_mes + timedelta(days=31) # usada para determinar o ultimo dia do mes
        # a função 'timedelta' permite adicionar uma qtde especifica de dias a uma data

        despesas_filtradas = [] # responsável por filtrar as despesas do mês vigente
        for despesa in despesas:
            # a função 'datetime.strptime' é usada para converter a string representando
            # a data de cada despesa para um objeto 'datetime'
            data_despesa = datetime.strptime(despesa['data'], '%Y-%m-%d')
            if primeiro_dia_do_mes <= data_despesa <= ultimo_dia_do_mes:
                despesas_filtradas.append(despesa)

        if despesas_filtradas: # Verifica se existe alguma despesa filtradas
            success = True
        else: #caso não exista, retorna false
            success = False

        responseBody = {
            'success': success,
            'data': despesas_filtradas
            }
        return jsonify(responseBody)

    app.register_blueprint(despesas_api, url_prefix='/api')
    return app
