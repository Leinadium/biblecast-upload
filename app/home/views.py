from flask import render_template, redirect, url_for
from . import home_blueprint


@home_blueprint.route("/", methods=['GET'])
def pagina_inicial():
    """Pagina inicial do sistema.

    Somente redireciona para a página de autenticação
    """
    return redirect('/auth')


@home_blueprint.route('/auth', methods=['GET', 'POST'])
def autenticacao():
    """Página de autenticação do usuário

    Carrega um formulário pedindo as credenciais da igreja
    """
    return render_template('index.html')
