import CHIP_IO.GPIO as GPIO
import time

from wiki_api import CalangoWiki
wiki = CalangoWiki()

def status_atual():
    """Verifica no site o status atual (aberto ou fechado)"""
    return wiki.conteudo_pagina("status")


def muda_status(status):
    """Atualiza a wiki com o status selecionado"""
    wiki.atualiza_pagina('status', status)



    #opções = 'Aberto Fechado'.split()
    

if __name__ == '__main__':

        GPIO.setup("CSID0",GPIO.IN) 
        while 1:
           if GPIO.input("CSID0"):
                   muda_status("Fechado")  
                   print("HIGH")
           else: 
                   muda_status("Aberto")  
                   print("LOW") 
           time.sleep(300)
                   
                   
