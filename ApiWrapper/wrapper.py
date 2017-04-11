import json
import os
import copy
from .currencies import currency_factory as curFac
from .apiCalls.caller import ApiCaller
from datetime import date
from datetime import timedelta

from threading import Thread
from time import sleep

'''
    Classe que envolve a as requisições da api e as moedas suportadas

    String path : caminho para o arquivo de configuração
    API Object api : api de base para as requisições
'''


class Wrapper:
    def __init__(self, path, api=None):

        self._api = api
        if not api:
            self._api = ApiCaller(self._configObj['api']['token'], *myCurrs)

        try:
            # abre o arquivo de configuração
            with open(path, 'r') as configFile:
                configJson = json.load(configFile)
                self._configObj = configJson

                dateAtt = self.fileObj(
                    os.path.join(configJson["resultDir"], ".lastAtt.txt"))
                # confere se o arquivo de data existe
                if not dateAtt:
                    self._dateAtt = date(1900, 1, 1)
                else:
                    self._dateAtt = date(
                        *[int(_i) for _i in dateAtt.readline().split('-')])

        except FileNotFoundError:
            raise RuntimeError("Config file not founded")

        except Exception:
            raise RuntimeError("Unexpected Error on read config file")

    '''
        chamada da thread que observa quando é preciso atualizar os dados
    '''
    def observe(self):
        thread = Thread(target=self._observeThread)
        thread.start()

    '''
        checa a cada 10h se os dados precisam ser atualizados
    '''
    def _observeThread(self):
        # checa a cada 10h se os dados precisam ser atualizados
        while(True):
            if not self._check():
                self._createObjHistory()
            sleep(36000)  # 10 horas

    '''
        checa a data dos arquivos e com a data atual
    '''
    def _check(self):
        if not self._dateAtt:
            return False
        elif (self._dateAtt - date.today()).days != 0:
            return False
        return True

    '''
        retorna as moedas suportadas
    '''
    def getCurrencies(self):
        return json.dumps({"currencies": self._configObj["api"]["currencies"]})

    '''
        pega o arquivo referente a uma moedas
        strign name : nome da moeda requisitada
    '''
    def getFile(self, name):
        try:
            myfile = open(
                os.path.join(self._configObj['resultDir'], name+'.txt',), 'r')
            return myfile.read()
        except Exception:
            return ''

    '''
        retorna um json do arquivo requisitado
        string method : metodo que deve ser chamado na api
        string file : nome da moeda requisitada
    '''

    def getObj(self, method, file):
        if method == "history":
            if self._check():
                return self._getObjHistory(file)
            else:
                self._createObjHistory()
                return self._getObjHistory(file)

    '''
        tenta achar o arquivo referente a uma moeda, se não achar ele tenta
        cria-lo

        string mfile : nome da moeda
        boolean recursive : caso True ele continua tentando achar/criar
                            o arquivo
    '''
    def _getObjHistory(self, mfile, recursive=True):
        try:
            myfile = self.fileObj(
                os.path.join(self._configObj['resultDir'], mfile+'.txt'))
            return json.load(myfile)
        except FileNotFoundError:
            self._createObjHistory()
            if recursive:
                _getObjHistory(self, file, False)
            else:
                raise RuntimeError("Can't create obj file")

    '''
        cria todos os arquivos referentes a cada moeda
    '''
    def _createObjHistory(self):
        myCurrs = []

        for currency in self._configObj['api']['currencies']:
            myCurrs.append(curFac.CurrencyFactory(currency))

        response = {}
        try:
            response = self._api.history(self._configObj["history"])
        except Exception:
            raise RuntimeError("Error on Api Call")

        myJson = json.load(self.fileObj(self._configObj['modelPath']))

        '''
            O(n)
            i = number of currencys
            j = number of data days
            each currency has n content

            like a matrix n*m
        '''
        for item in myCurrs:
            thisCurrency = copy.deepcopy(myJson)
            for jsonResponse in response["response"]:
                thisCurrency["series"][0]["data"]\
                    .append(
                        jsonResponse["quotes"]['USD'+str(item)]
                    )
            thisCurrency["title"]["text"] =\
                self._configObj["api"]["titles"][str(item)]

            thisCurrency["series"][0]["pointStart"] =\
                int((date.today() - timedelta(days=7)).strftime("%s"))*1000

            self.file_creator(
                    os.path.join(
                        self._configObj['resultDir'], (str(item) + '.txt')),
                    json.dumps(thisCurrency))

        todayCurrency = self._api.live()

        self.file_creator(
                    os.path.join(self._configObj['resultDir'], 'TODAY.txt'),
                    json.dumps(todayCurrency))

        self.file_creator(
                    os.path.join(self._configObj['resultDir'], '.lastAtt.txt'),
                    date.today().isoformat())

    '''
        cria um arquivo dando o caminho e conteúdo
        string path : caminho do arquivo
        string content : conteúdo a ser escrito
    '''
    def file_creator(self, path, content):
        try:
            with open(path, 'w') as arq:
                arq.write(content)
        except FileNotFoundError:
            print("Can't write file: %s" % path)
        except Exception:
            raise RuntimeError("Unexpected Error on file create")

    '''
        abre uma arquivo e returna sua estrutura
        strin path : caminho do arquivo
    '''
    def fileObj(self, path):
        try:
            obj = open(path, 'r')
            return obj
        except FileNotFoundError:
            print("File not founded")
        except Exception:
            raise RuntimeError("Unexpected Error on file read")

    '''
        abre um arquivo e retorna seu conteúdo
    '''
    def readFile(self, path):
        try:
            with open(path, 'r') as arq:
                return arq.read()
        except FileNotFoundError:
            print("File not founded")
