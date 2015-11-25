# coding: utf-8
import requests
"""
    Permite informar no site do Calango se o hackerspace está aberto
       ou fechado.

    Disponibiliza uma interface em que o usuário diz se o Calango está
       aberto ou fechado.

    Acessa o site do Calango e verifica se ele está aberto ou fechado.

    Se a situação informada no site for diferente da informada pelo
       usuário, atualiza o site com a informação do usuário.
"""


def obter_credenciais():
    """Obtém usuário e senha de um arquivo"""
    with open('credenciais.txt') as arquivo:
        usuario = arquivo.readline().strip()
        senha = arquivo.readline().strip()
    return (usuario, senha)

if __name__ == '__main__':
    (usuario, senha) = obter_credenciais()
    r = requests.get('http://calango.club/status', auth=(usuario, senha))
    r.status_code
    r = requests.get('http://calango.club/status?do=export_raw')
    print(r.text)
