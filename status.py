#! /usr/bin/env python3
# coding: utf-8
"""
    Permite informar no site do Calango se o hackerspace está aberto
       ou fechado.

    (TODO) Disponibiliza uma interface em que o usuário diz se o Calango está
       aberto ou fechado.

    Acessa o site do Calango e verifica se ele está aberto ou fechado.

    Se a situação informada no site for diferente da informada pelo
       usuário, atualiza o site com a informação do usuário.
"""

import requests
from bs4 import BeautifulSoup


def obter_credenciais():
    """Obtém usuário e senha de um arquivo"""
    with open('credenciais.txt') as arquivo:
        usuario = arquivo.readline().strip()
        senha = arquivo.readline().strip()
    return (usuario, senha)


def status_atual():
    """Verifica no site o status atual (aberto ou fechado)"""
    r = requests.get('http://calango.club/status?do=export_raw')
    return r.text


def atualiza_pagina(url, id_pagina, conteudo):
    
    # cria a sessão
    s = requests.Session()
    (usuario, senha) = obter_credenciais()
    s.auth = (usuario, senha)
    
    r = s.get(url)

    # localiza o token da sessão na página
    soup = BeautifulSoup(r.content, 'html.parser')
    sectok = soup.find('input', {'name':'sectok'})['value']
    
    payload = {'id': id_pagina, 'rev': '0', 'prefix': '.',
               'sectok': sectok, 'wikitext': conteudo}
    url = 'http://calango.club/%s?do=save' %id_pagina
    
    return s.post(url, data=payload)
    
def muda_status(status):
    pass

if __name__ == '__main__':

    print(status_atual())

    # acessa a página de edição e obtém o form com o token
    url = 'http://calango.club/status?do=edit'

    atualiza_pagina(url, 'status', 'ativo')
    
