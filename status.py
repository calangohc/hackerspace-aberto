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
import urwid
from bs4 import BeautifulSoup
from urllib.parse import urljoin


DOMINIO = 'http://calango.club'


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


def atualiza_pagina(id_pagina, conteudo):

    # cria a sessão
    s = requests.Session()
    (usuario, senha) = obter_credenciais()
    s.auth = (usuario, senha)

    url = urljoin(DOMINIO, id_pagina)
    r = s.get(url, params={'do': 'edit'})

    # localiza o token da sessão na página
    soup = BeautifulSoup(r.content, 'html.parser')
    sectok = soup.find('input', {'name': 'sectok'})['value']

    payload = {'id': id_pagina, 'rev': '0', 'prefix': '.',
               'sectok': sectok, 'wikitext': conteudo}

    return s.post(url, data=payload, params={'do': 'save'})


def muda_status(status):

    atualiza_pagina('status', status)


def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    muda_status(choice)
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()


if __name__ == '__main__':

    choices = 'Aberto Fechado'.split()

    main = urwid.Padding(menu(u'Status Calango', choices), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                        align='center', width=('relative', 60),
                        valign='middle', height=('relative', 60),
                        min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

