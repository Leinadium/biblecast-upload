from flask import Flask, _app_ctx_stack     # noqa
import json
from warnings import warn


from typing import Optional, Dict, List


class Database:
    """Classe para implementação de uma base de dados para o site"""

    def __init__(self, app: Optional[Flask] = None):
        """Inicializa a base de dados"""
        self._slugs: Dict[str, str] = dict()
        self._chaves: Dict[str, str] = dict()
        self._chaves_invertidas: Dict[str, str] = dict()      # para encontrar a igreja pela chave
        self._telefones: Dict[str, List[str]] = dict()
        self._series: Dict[str, List[str]] = dict()
        self._pastores: Dict[str, List[str]] = dict()

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Inicializa o objeto Database com as configurações do Flask"""
        # tentando abrir o arquivo completo
        path_arquivo_de_configuracao: Optional[str] = app.config.get("CONFIG_JSON_FILE")
        if path_arquivo_de_configuracao is None:
            warn("Path para arquivo de configuração não definido")
            return

        # parsing do arquivo
        try:
            with open(path_arquivo_de_configuracao, 'r', encoding='UTF-8') as arquivo:
                dicionario_configuracao: dict = json.load(arquivo)

            # preenchendo as variaveis
            for nome_igreja, conteudo_igreja in dicionario_configuracao.items():
                self._slugs[nome_igreja] = conteudo_igreja['slug']
                self._chaves[nome_igreja] = conteudo_igreja['chave']
                self._chaves_invertidas[conteudo_igreja['chave']] = nome_igreja
                self._telefones[nome_igreja] = conteudo_igreja['telefone']
                self._series[nome_igreja] = conteudo_igreja['series']
                self._pastores[nome_igreja] = conteudo_igreja['pastores']

        except json.JSONDecodeError:
            warn("Arquivo de configuração inválido")
        except FileNotFoundError:
            warn(f"Arquivo de configuração {path_arquivo_de_configuracao} não encontrado")
        except KeyError as e:
            warn(f"Chave não encontrada no arquivo de configuração: {e}")

    def get_nome_igreja(self, chave: str) -> Optional[str]:
        """Retorna o nome da igreja a partir da chave"""
        return self._chaves_invertidas.get(chave)


