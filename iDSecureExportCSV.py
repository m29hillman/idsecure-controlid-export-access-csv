import time
import shutil
from os import listdir
from os.path import isfile, join, basename
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#PASTA DE ORIGEM
origem = 'C:/Users/usuario/Downloads' 
#PASTA DE REDE
destino = '\\\\caminho.rede.com.br\\pasta'

#DEFINIDO FILTRA PELA DATA DO DIA ANTERIOR
presentday = datetime.now() 
yesterday = presentday - timedelta(1) 
print(yesterday.strftime('%d/%m/%Y'))

#DEFINE QUE O NAVEGADOR IRA IGNORAR ERROS DE CERTIFICADOS
profile = webdriver.ChromeOptions()
profile.add_argument('--ignore-certificate-errors')
profile.add_argument('--ignore-ssl-errors')

#DEFINE O NAVEGADOR E ABRE A PAGINA INICIAL
navegador = webdriver.Chrome(options=profile)
navegador.get("https://localhost:30443/#/login")

#PASSO A PASSO PARA REALIZAR O LOGIN
time.sleep(2.5)
fldUsuario = navegador.find_element(By.ID, "usr")
fldUsuario.send_keys("user")
fldSenha = navegador.find_element(By.ID, "pwd")
fldSenha.send_keys("password")
btnEntrar = navegador.find_element(By.ID, "entrar")
btnEntrar.click()

#PAGINA DE RELATORIOS DE ACESSO
time.sleep(2.5)
navegador.get("https://localhost:30443/#/view_report/global")
time.sleep(2.5)

#CONFIGURA FILTROS AVANCADOS
buscaAvancada = navegador.find_element(By.ID, "btn_advFilter")
buscaAvancada.click()
time.sleep(2.5)
dataInicial = navegador.find_element(By.ID, "initialDate")
dataInicial.clear();
dataInicial.send_keys(yesterday.strftime('%d/%m/%Y'))
dataFinal = navegador.find_element(By.ID, "finalDate")
dataFinal.clear();
dataFinal.send_keys(yesterday.strftime('%d/%m/%Y'))
dispositivos =  navegador.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div/div[4]/div[2]/div[3]/div/div[7]/div/div/input") 
dispositivos.clear();
dispositivos.send_keys("Refeitorio")
dispositivos.send_keys(Keys.ENTER)
tpRegistros = navegador.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/div/div[1]/div/div[4]/div[2]/div[3]/div/div[9]/div/div/input")
tpRegistros.clear();
tpRegistros.send_keys("Autorizado")
tpRegistros.send_keys(Keys.ENTER)

#APLICA FILTROS AVANCADOS
time.sleep(2.5)
btnListar = navegador.find_element(By.ID, "btn_report_list")
btnListar.click()

#GERA CSV
time.sleep(2.5)
btnExporta = navegador.find_element(By.ID, "btn_export")
btnExporta.click()
time.sleep(2.5)
btnGeraCsv = navegador.find_element(By.ID, "btn_export_csv")
btnGeraCsv.click()

time.sleep(5)

#FECHA NAVEGADOR
navegador.close()

time.sleep(2.5)

#COPIA CSV PARA A PASTA INFORMADA
for item in [join(origem, f) for f in listdir(origem) if isfile(join(origem, f)) and f.endswith('csv')]:
    #print(item)
    shutil.move(item, join(destino, basename(item)))
    print('moved "{}" -> "{}"'.format(item, join(destino, basename(item))))

