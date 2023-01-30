from json import dumps
from unidecode import unidecode
from flask import render_template, redirect, request, session

from .. import db
from . import home_blueprint
from .forms import Formulario
from .generate import gerar_dados_finais, salvar


@home_blueprint.route("/", methods=["GET", "POST"])
def index():
    if session.get("igreja") is not None:
        return redirect('/form')
    else:
        return redirect('/auth')


@home_blueprint.route("/form-antigo", methods=['GET', "POST"])
def view_form_antigo():
    """Pagina inicial do sistema.

    Somente redireciona para a página de autenticação
    """
    igreja = session.get("igreja")
    if igreja is None:
        return redirect('/auth')

    pregadores = db.get_pastores(chave=igreja)
    series = db.get_series(chave=igreja)

    return render_template(
        'main.html',
        igreja=igreja,
        pregadores=pregadores,
        series=series
    )


@home_blueprint.route("/form", methods=["GET", "POST"])
def view_form():
    formulario = Formulario()

    igreja = session.get("igreja")
    if igreja is None:
        return redirect('/auth')

    pregadores = db.get_pastores(chave=igreja)
    series = db.get_series(chave=igreja)

    formulario.pregador.choices.extend(list(zip(pregadores, pregadores)))
    formulario.serie.choices.extend(list(zip(series, series)))

    if formulario.validate_on_submit():
        # verificando dados
        json_final = gerar_dados_finais(igreja, formulario)
        mensagem_telegram = "[biblecast.net] Foi recebido para o tratamento o arquivo de áudio " \
                            f"referente à mensagem de {json_final['data']} com o título " \
                            f"{json_final['titulo']}. Você receberá " \
                            "uma notificação quando essa mensagem foi publicada com sucesso."

        slug = db.get_slug(igreja)
        pastor = unidecode(
            json_final['pregador'],
            errors='replace',
            replace_str='00'
        ).lower().replace(' ', '-')
        data_formatada = formulario.data.data.strftime("%Y%m%d") + json_final['turno']
        nome_arquivo = f'{data_formatada}-{igreja}-{pastor}.json'

        salvar(json_final, nome_arquivo)

        json_final_str = dumps(json_final, indent=2)

        return render_template('success.html', msg=mensagem_telegram, json=json_final_str)

    return render_template('main2.html', form=formulario, igreja=igreja)


@home_blueprint.route('/auth', methods=['GET', 'POST'])
def autenticacao():
    """Página de autenticação do usuário

    Carrega um formulário pedindo as credenciais da igreja
    """
    if request.args.get('reset'):
        session['igreja'] = None

    if request.method == 'POST':
        chave = request.form.get("chave")

        igreja = db.get_nome_igreja(chave=chave)
        if igreja is None:
            return render_template('auth.html', erro=True)

        session['igreja'] = igreja
        return redirect('/form')

    return render_template('auth.html')
