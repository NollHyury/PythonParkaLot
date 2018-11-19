'''
Created on 18 de nov de 2018

@author: hyury

'''
import json
from bson.int64 import long
import datetime
from _datetime import date, timedelta

valorPadrao = 2
valorTaxaCarroHora = 2.50 
valorTacaMotoHora = 1.50
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
    preencherVaga(auto['tipoDoAutomovel'])
    
    
    
    
def verAutomoveisEstacionados():
    AutomoveisEstacionados = carregarJsonDosEstacionados()
    return AutomoveisEstacionados
    

def buscarInformacoesDeVagasLivres():
    f = open("vagasLivres", "r")
    retorno = f.read()
    f.close()
    return int(retorno)

def preencherVaga(quantia):
    novosDados = buscarInformacoesDeVagasLivres() - quantia
    f = open("vagasLivres","w")
    f.write(str(novosDados))
    f.close()
    
def reporVagas(quantia):
    f = open("vagasLivres","w")
    novosDados = buscarInformacoesDeVagasLivres() + quantia
    f.write(str(novosDados))
    f.close()

def verificarDisponibilidade(codigoDoAutomovel):
    vagasLivres = buscarInformacoesDeVagasLivres()
    if(vagasLivres>=2 and codigoDoAutomovel == codigoCarro):
        return True
    elif(vagasLivres >=1 and codigoDoAutomovel == codigoMoto):
        return True
    else:
        return False
    
def registrarJson(listaEstacionados):
    f = open("jsonEstacionados","w")
    f.write(json.dumps(listaEstacionados))
    f.close()
    
def carregarJsonDosEstacionados():
    f = open("jsonEstacionados","r")
    auto = json.loads(f.read())
    f.close()
    return auto
    
def retirarAutomovelDoEstacionamento():
    buscarPlaca = str(input('digite a placa do automovel:'))
    AutomoveisEstacionados = carregarJsonDosEstacionados()
    for automovel in AutomoveisEstacionados:
        if(automovel['placa'] == buscarPlaca):
            print(automovel['horaDeEntrada'])
            cobrarTaxaDeEstacionamento(automovel['tipoDoAutomovel'], automovel['horaDeEntrada'])
            AutomoveisEstacionados.remove(automovel)
            registrarJson(AutomoveisEstacionados)
            reporVagas(automovel['tipoDoAutomovel'])
            return 'Obrigado, volte Sempre!'
    else:
        return 'falha na busca digite uma placa valida'

def cobrarTaxaDeEstacionamento(codigoAutomovel,horaDeEntrada):
    horaAtual = datetime.datetime.now()
    horaDeComparacao = datetime.datetime.strptime(horaDeEntrada, "%Y-%m-%d %H:%M:%S.%f")
    totalDeHoras = horaAtual - horaDeComparacao
    print(totalDeHoras)
    if(totalDeHoras < timedelta(hours = 1)):
        print('deve ser cobrado uma taxa de:',valorPadrao)
    else:
        horaAcumulada = 1
        valorPagar = valorPadrao
        while(totalDeHoras > timedelta(hours = horaAcumulada)):
            horaAcumulada = horaAcumulada +1
            valorPagar = valorPagar + pagamentoPorTipoDeAutomovel(codigoAutomovel)
        print('deve ser cobrado uma taxa de:',valorPagar)
        
def pagamentoPorTipoDeAutomovel(codigo):
    if(codigo == codigoCarro):
        return valorTaxaCarroHora
    else:
        return valorTaxaCarroHora    
    
estacionar()
print(verAutomoveisEstacionados())
    
#retirarAutomovelDoEstacionamento('7484')
