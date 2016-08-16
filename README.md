# hackerspace-aberto
Publica na internet situação do hackerspace (se aberto ou fechado)

#Configuracao da inicializacao do sensor de porta 
Copiar initSensorPorta para /etc/init.d
Copiar initSensorPorta.service para /etc/systemd/system

#Ativar inicializacao no boot do C.H.I.P.
sudo systemctl enable initSensorPorta.service
