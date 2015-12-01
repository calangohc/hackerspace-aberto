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

import urwid
from wiki_api import CalangoWiki

wiki = CalangoWiki()

def status_atual():
    """Verifica no site o status atual (aberto ou fechado)"""
    return wiki.conteudo_pagina("status")


def muda_status(status):
    """Atualiza a wiki com o status selecionado"""
    # TODO Verificar o status atual antes para evitar atualização desnecessária
    wiki.atualiza_pagina('status', status)


def cria_menu(título, opções):
    """Interface do Urwid"""
    corpo = [urwid.Text(título), urwid.Divider()]
    for opção in opções:
        botão = urwid.Button(opção)
        # vincula o botão à chamada de escolhe_opção() passando a
        # opção escolhida e o botão pressionado
        urwid.connect_signal(botão, 'click', escolhe_opção, opção)
        # desenha o botão
        corpo.append(urwid.AttrMap(botão, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(corpo))


def escolhe_opção(botão, escolha):
    """Ação disparada pela seleção de uma opção"""
    response = urwid.Text(['Status alterado para ', escolha, '\n'])
    muda_status(escolha)
    botao_ok = urwid.Button('Ok')
    # vincula o botão "Ok" ao seu callback
    urwid.connect_signal(botao_ok, 'click', reinicia)
    # inclui o botão "Ok" na janela
    janela.original_widget = \
        urwid.Filler(
            urwid.Pile([response,
                        urwid.AttrMap(botao_ok, None,
                                      focus_map='reversed')]))


def reinicia(button):
    janela.original_widget = cria_janela()


def exit_program(button):
    raise urwid.ExitMainLoop()


def cria_janela():
    # janela contém menu

    opções = 'Aberto Fechado'.split()
    
    menu = cria_menu("Status Calango (%s)" % status_atual(), opções)
    return urwid.Padding(menu, left=2, right=2)


def cria_interface(janela):
    # tela é o widget principal do urwid e contém janela
    return urwid.Overlay(janela, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                         align='center', width=('relative', 60),
                         valign='middle', height=('relative', 60),
                         min_width=20, min_height=9)


if __name__ == '__main__':
    janela = cria_janela()
    urwid.MainLoop(cria_interface(janela),
                   palette=[('reversed', 'standout', '')]).run()
