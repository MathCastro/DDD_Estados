from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.by import By as SeleniumBy
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common import exceptions as s_exc
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.remote.remote_connection import LOGGER as SELENIUM_LOGGER
# Importar classe para ajudar a localizar os elemen# Importar a classe que contém as funções e aplicar um alias
from selenium.webdriver.support import expected_conditions as ECtos
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    StaleElementReferenceException, NoSuchElementException, WebDriverException,
    TimeoutException, InvalidElementStateException, NoSuchAttributeException, ElementClickInterceptedException
)

driver = webdriver.Chrome()

wait = WebDriverWait(driver, 120)

driver.get('http://www.ddi-ddd.com.br/Codigos-Telefone-Brasil/')

elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'centre2')))
estados = format(elem.text)
estados = estados.split('\n')
estados.pop(0)
dddTotal = []
regiaoNorte = ['AM','RR','AP','PA','TO','RO','AC']
regiaoNordeste = ['MA', 'PI','CE','RN','PE','PB','SE','AL','BA']
regiaoCentroOeste = ['MT','MS','GO']
regiaoSudeste = ['SP','RJ','ES','MG']
regiaoSul = ['PR','RS','SC']
arquivo = open('sql.txt', 'w')
for estado in estados:
    dddEstado = []
    estado = estado[1:]
    elem = wait.until(EC.presence_of_element_located((By.LINK_TEXT, estado)))
    elem.click()
    infos = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tabela_regioes_cidades')))
    infos = format(infos.text)
    infos = infos.split('\n')
    for info in infos:
        info = info.split(" ")
        if(not(info[len(info)-1] in dddEstado)):
            dddEstado.append(info[len(info)-1])
        if(info[0] in regiaoNorte):
            regiao = "1"
        elif(info[0] in regiaoNordeste):
            regiao = "2"
        elif(info[0] in regiaoCentroOeste):
            regiao = "3"
        elif(info[0] in regiaoSudeste):
            regiao = "4"
        elif(info[0] in regiaoSul):
            regiao = "5"
    dddEstado.pop(0)
    dddEstado.sort()
    informacoes = {
        "Região" : regiao,
        "Estado" : estado,
        "UF" : info[0],
        "DDD" : dddEstado
    }
    dddTotal.append(informacoes)
    print(informacoes)
    if(estado == "Ceará (CE)"):
        informacoes = {
            "Região" : 3,
            "Estado" : "Distrito Federal (DF)",
            "UF" : "DF",
            "DDD" : ['61']
        }
        dddTotal.append(informacoes)
        print(informacoes)
sql = "INSERT INTO TB_REGION(ID,NAME) VALUES(" + "1, " + "\'Norte\');\n"
arquivo.writelines(sql)
sql = "INSERT INTO TB_REGION(ID,NAME) VALUES(" + "2, " + "\'Nordeste\');\n"
arquivo.writelines(sql)
sql = "INSERT INTO TB_REGION(ID,NAME) VALUES(" + "3, " + "\'Centro-Oeste\');\n"
arquivo.writelines(sql)
sql = "INSERT INTO TB_REGION(ID,NAME) VALUES(" + "4, " + "\'Sudeste\');\n"
arquivo.writelines(sql)
sql = "INSERT INTO TB_REGION(ID,NAME) VALUES(" + "5, " + "\'Sul\');\n"
arquivo.writelines(sql)

contador = 1
for elemento in dddTotal:
    name = elemento['Estado'][:len(elemento['Estado'])-5]
    sql = "INSERT INTO TB_STATE(ID, NAME, UF, ID_REGION) VALUES (" + str(contador) + ",\'" + name + "\'," + "\'" + elemento['UF'] + "\'," + str(elemento['Região']) + ");\n"
    arquivo.writelines(sql)
    contador = contador + 1

estado = 1
contador = 1
for elemento in dddTotal:
    for ddd in elemento['DDD']:
        sql = "INSERT INTO TB_AREA_CODE(ID, CODE, ID_STATE) VALUES (" + str(contador) + "," + str(ddd) + "," + str(estado) + ");\n"
        arquivo.writelines(sql)
        contador = contador + 1
    estado = estado + 1


arquivo.close()