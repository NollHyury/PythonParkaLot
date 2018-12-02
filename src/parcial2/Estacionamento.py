'''
Created on 18 de nov de 2018

@author: hyury

'''
import os.path
import json
import datetime
from _datetime import date, timedelta
from bson.int64 import long


valorPadrao = 2
valorTaxaCarroHora = 2.50 
valorTaxaMotoHora = 1.50
codigoCarro = 2
codigoMoto = 1
AutomoveisEstacionados = []

def criarAutomovel():
    placa = str(input('digite a placa do automovel:'))
    modelo = str(input('digite o modelo do automovel:'))
    propietario = str(input('digite o nome do propietario:'))
    telefone = long(input('digite o telefone do propietario:'))
    cpf = long(input('digite o cpf do propietario:'))
    tipoDoAutomovel = int(input("digite (1) para moto e (2) para Carro;"))
    
    veiculo = {
    'placa' :placa ,
    'modelo' : modelo,
    'propietario' : propietario,
    'telefone' : telefone,
    'cpf' : cpf,
    'horaDeEntrada' : datetime.datetime.now().__str__(),
    'tipoDoAutomovel' : tipoDoAutomovel
    }
    
    return veiculo



def estacionar():
    AutomoveisEstacionados = carregarJsonDosEstacionados()
    auto = criarAutomovel()
    verificarDisponibilidade(auto['tipoDoAutomovel'])
    AutomoveisEstacionados.append(auto)
    registrarJson(AutomoveisEstacionados)
    print('vagas sobrando: ', validarVagas())
    
def verAutomoveisEstacionados():
    AutomoveisEstacionados = carregarJsonDosEstacionados()
    for veiculo in AutomoveisEstacionados:
        print(veiculo)
    

def validarVagas():
    vagasTotais = 120
    
    AutomoveisEstacionados = carregarJsonDosEstacionados()
    for veiculo in AutomoveisEstacionados:
        if(veiculo['tipoDoAutomovel']== codigoCarro):
            vagasTotais = vagasTotais - 2
        else:
            vagasTotais = vagasTotais - 1
    
    return vagasTotais


def verificarDisponibilidade(codigoDoAutomovel):
    vagasLivres = validarVagas()
    if(vagasLivres>= codigoCarro and codigoDoAutomovel == codigoCarro):
        return True
    elif(vagasLivres >=codigoMoto and codigoDoAutomovel == codigoMoto):
        return True
    else:
        return False
    
def registrarJson(listaEstacionados):
    f = open("jsonEstacionados","w")
    f.write(json.dumps(listaEstacionados))
    f.close()
    
def carregarJsonDosEstacionados():
    if(os.path.isfile('jsonEstacionados')):
        f = open("jsonEstacionados","r")
        auto = (f.read())
        f.close()
        return json.loads(auto)
    else:
        registrarJson([])
        return carregarJsonDosEstacionados()
    
def retirarAutomovelDoEstacionamento():
    buscarPlaca = str(input('digite a placa do automovel:'))
    AutomoveisEstacionados = carregarJsonDosEstacionados()
    for automovel in AutomoveisEstacionados:
        if(automovel['placa'] == buscarPlaca):
            print(automovel['horaDeEntrada'])
            cobrarTaxaDeEstacionamento(automovel['tipoDoAutomovel'], automovel['horaDeEntrada'])
            AutomoveisEstacionados.remove(automovel)
            registrarJson(AutomoveisEstacionados)
            print('Obrigado, volte Sempre!','vagas sobrando: ', validarVagas())
            
        else:
            print('falha na busca digite uma placa valida')

def cobrarTaxaDeEstacionamento(codigoAutomovel,horaDeEntrada):
    horaAtual = datetime.datetime.now()
    horaDeComparacao = datetime.datetime.strptime(horaDeEntrada, "%Y-%m-%d %H:%M:%S.%f")
    totalDeHoras = horaAtual - horaDeComparacao
    print('seu automovel ficou estacionado por:',totalDeHoras,'H')
    print('................................................................................')
    if(totalDeHoras < timedelta(hours = 1)):
        print('deve ser cobrado uma taxa de:',valorPadrao,'R$ pelo estacionamento.')
    else:
        horaAcumulada = 1
        valorPagar = valorPadrao
        while(totalDeHoras > timedelta(hours = horaAcumulada)):
            horaAcumulada = horaAcumulada +1
            valorPagar = valorPagar + pagamentoPorTipoDeAutomovel(codigoAutomovel)
        print('deve ser cobrado uma taxa de:',valorPagar,'R$ pelo estacionamento.')
        
def pagamentoPorTipoDeAutomovel(codigo):
    if(codigo == codigoCarro):
        return valorTaxaCarroHora
    else:
        return valorTaxaMotoHora 
    

openSystem = True
while(openSystem):
    print('voce deseja estacionar ou retirar o seu veiculo?')
    opcao = str(input('Para estacionar digite [E], para Retirar digite [R],para consultar digite [C] e para Sair do sistema digite [S]'))
    if(opcao.upper() == 'S'):
        openSystem = False
        break
    elif(opcao.upper() == 'E'):
        estacionar()
    elif(opcao.upper() == 'R'):
        retirarAutomovelDoEstacionamento()
    elif(opcao.upper()=='C'):
        verAutomoveisEstacionados()
    else:
        print('voce noo digitou uma opcao valida, favor vericar.')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    


