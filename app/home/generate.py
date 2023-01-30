from json import dump
from os import environ, path
from .forms import Formulario, VALOR_NULO, VALOR_OUTROS

DIRETORIO_PADRAO = './'
ENV_NAME = 'PASTA_DICIONARIOS'


def gerar_dados_finais(igreja: str, form: Formulario) -> dict:
    ret = dict()
    ret['igreja'] = igreja
    ret['url'] = form.url.data
    ret['data'] = form.data.data.isoformat()
    ret['turno'] = form.turno.data if form.turno.data != VALOR_OUTROS else form.turno_alt.data
    ret['titulo'] = form.titulo.data
    ret['pregador'] = form.pregador.data if form.pregador.data != VALOR_OUTROS else form.pregador_alt.data
    if form.serie.data == VALOR_OUTROS:
        ret['serie'] = form.serie_alt.data
    elif form.serie.data == VALOR_NULO:
        ret['serie'] = ''
    else:
        ret['serie'] = form.serie.data
    ret['inicio'] = str(form.inicio.data) if form.inicio.data != VALOR_NULO else ''
    ret['fadeIn'] = form.fade_in.data
    ret['fim'] = str(form.fim.data) if form.fim.data != VALOR_NULO else ''
    ret['fadeOut'] = form.fade_out.data
    ret['comentario'] = form.comentario.data

    return ret


def salvar(dicionario: dict, filename: str):
    if 'PASTA_DICIONARIOS' not in environ:
        dirr = DIRETORIO_PADRAO
    else:
        dirr = environ.get('PASTA_DICIONARIOS')

    path_final = path.join(dirr, filename)

    with open(path_final, 'w+', encoding='utf-8') as f:
        dump(dicionario, f, indent=2)
    return
