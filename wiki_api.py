#! /usr/bin/env python3
# coding: utf-8
"""
    Atualizar o site do Calango programaticamente

"""

import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

DOMINIO = 'http://calango.club'

class CalangoWiki :
    """API do Wiki do Calango"""

    def __init__(self) :
        self.usuario, self.senha = self.obter_credenciais()

    def obter_credenciais(self):
        """Obtém usuário e senha de um arquivo"""
        with open('credenciais.txt') as arquivo:
            usuario = arquivo.readline().strip()
            senha = arquivo.readline().strip()
        return (usuario, senha)

    def conteudo_pagina(self,id_pagina) :
        """A conteudo do pagina"""
        return requests.get('http://calango.club/%s?do=export_raw' % id_pagina).text
            
        
    def atualiza_pagina(self,id_pagina, conteudo):
        """Modificador genérico de páginas da wiki"""
        # cria a sessão
        s = requests.Session()
        s.auth = (self.usuario, self.senha)

        # monta a url como dominio/pagina
        url = urljoin(DOMINIO, id_pagina)
        r = s.get(url, params={'do': 'edit'})

        # localiza o token da sessão na página
        soup = BeautifulSoup(r.content, 'html.parser')
        sectok = soup.find('input', {'name': 'sectok'})['value']

        wikitext = "{{ :status:imagens:%s.png?nolink&300 |}}" \
                    % conteudo.lower()
        # conteúdo do form a ser submetido
        payload = {'id': id_pagina, 'rev': '0', 'prefix': '.',
                   'sectok': sectok, 'wikitext': wikitext}

        return s.post(url, data=payload, params={'do': 'save'})
    
