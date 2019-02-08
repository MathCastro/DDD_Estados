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
from datetime import datetime, timedelta
import random
from tqdm import tqdm

apiName = ['sendSms', 'getAD', 'changeMSISDN', 'getSubscription', 'StartCallNotification']
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

arquivo = open('sql.txt', 'r')
sql = open('sql.txt', 'w')

for api in tqdm(apiName):
    for estado in range(1,28):
        for day in range(1,31):
            for hour in range(0,24):
                date_N_days_ago = datetime.now() - timedelta(days=day)
                dateBeforeTreatment = str(date_N_days_ago).split(' ')[0].split('-')
                date = dateBeforeTreatment[2] + "/" + dateBeforeTreatment[1] + "/" + dateBeforeTreatment[0]
                sql.writelines("INSERT INTO SDP_LOG_DISPLAY.TB_LOG_COUNTER (API_NAME,LOG_DATE,LOG_HOUR,ID_STATE,COUNTER) VALUES (" + "\'" + api + "\'" + ", to_date(\'" + date + "\'," + "\'DD/MM/RR\')," + "\'" + str(hour) + "\'," + "\'" + str(estado) + "\'," + "\'" + str(random.randint(0,5000)) + "\'" + ");\n")

