__version__ = '0.1'
__author__ = 'JoseChGal'

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import time

from connector import get_data_comuna, get_data_region, insert_data

def parseInt(value):

	value = value.replace('.','')
	return int(value)

def parseFloat(value):
	value = value.replace(',','.')
	value = value.replace('%','')
	return float(value)


def get_data_from_browser(browser):

	cantidad_poblacion = parseInt(browser.find_element_by_xpath('.//*[@id="valorpoblacion"]').text)
	cantidad_viviendas = parseInt(browser.find_element_by_xpath('.//*[@id="valirvivienda"]').text)
	cantidad_hombres = parseInt(browser.find_element_by_xpath('.//*[@id="valorhombres"]').text)
	cantidad_mujeres = parseInt(browser.find_element_by_xpath('.//*[@id="valoresmujer"]').text)
	densidad_poblacion = parseFloat(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[1]/div/table/tbody/tr[1]/td[2]').text)
	residentes_migrantes = parseInt(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[4]/div/table/tbody/tr[1]/td[2]').text)
	porcentaje_poblacion_migrante = parseFloat(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[4]/div/table/tbody/tr[4]/td[2]').text)
	porcentaje_pueblos_originarios = parseFloat(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[1]/div/table/tbody/tr[7]/td[2]').text)
	porcentaje_empleo_mujeres = parseFloat(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[6]/div/table/tbody/tr[3]/td[2]').text)
	porcentaje_hacinamiento = parseFloat(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]').text)
	cantidad_hogares = parseInt(browser.find_element_by_xpath('./html/body/div/div[2]/div[1]/div[2]/div[3]/div/table/tbody/tr[1]/td[2]').text)

	return {
		'cantidad_habitantes': cantidad_poblacion,
		'cantidad_viviendas':cantidad_viviendas,
		'cantidad_hombres': cantidad_hombres,
		'cantidad_mujeres': cantidad_mujeres,
		'densidad_poblacion': densidad_poblacion,
		'residentes_migrantes': residentes_migrantes,
		'porcentaje_poblacion_migrante': porcentaje_poblacion_migrante,
		'porcentaje_pueblos_originarios': porcentaje_pueblos_originarios,
		'porcentaje_empleo_mujeres': porcentaje_empleo_mujeres,
		'porcentaje_hacinamiento': porcentaje_hacinamiento,
		'cantidad_hogares': cantidad_hogares,
		'anio_censo':2017
	}

	

def get_data_from_web(url, numero_region):

	browser = webdriver.Chrome(ChromeDriverManager("2.36").install())
	timeout = 2

	#Se utilizan para enrutar a url api (POST) de inserción para datos de censo según caso de inserción y obtención desde BASE DE DATOS (API, conexión BD)
	#No necesario en caso de no utilizar API
	url_api_1 = 'datos_regiones_censo/'
	url_api_2 = 'datos_comunas_censo/'


	browser.get(url) 
	print('Extrayendo data...')
	print(f'Región: {numero_region}')
	n_region = int(numero_region)

	#Extracción datos censo según región
	data_extraida_region = get_data_from_browser(browser)
	
	
	#En este apartado se obtiene el ID de la REGIÓN para agregar
	#este a data extraida y generar el JSON de inserción para los datos REGIONALES
	#get_data_region se obtiene desde connector, modificar según caso de inserción y obtención desde BASE DE DATOS (API, conexión BD)
	data_region = get_data_region(n_region)
	id_region = data_region['id']

	#Se asigna ID REGIÓN  a objeto con data extraida
	data_extraida_region['region'] = id_region

	#Función para insertar JSON en punto POST según caso de inserción y obtención desde BASE DE DATOS (API, conexión BD)
	insert_data(url_api_1,data_extraida_region)

	comunas_select = browser.find_element_by_xpath('.//*[@id="comobocomunas"]')
	comunas_object = Select(comunas_select)
	comunas_disponibles = comunas_object.options
	cant_comunas_disponibles = len(comunas_disponibles)

	for i in range(1,cant_comunas_disponibles):
		comunas_object.select_by_index(i)
		comuna = comunas_disponibles[i]
		codigo_comuna = comuna.get_attribute("value")

		#En este apartado se obtiene el ID de la COMUNA para agregar
		#este a data extraida y generar el JSON de inserción para los datos COMUNALES
		#get_data_comuna se obtiene desde connector, modificar según caso de inserción y obtención desde BASE DE DATOS (API, conexión BD)
		data_comuna = get_data_comuna(codigo_comuna)
		id_comuna = data_comuna['id']

		#Extracción datos censo según comuna
		data_extraida_comuna = get_data_from_browser(browser)

		#Se asigna ID REGIÓN  a objeto con data extraida
		data_extraida_comuna['comuna'] = id_comuna
		#Se asigna ID COMUNA  a objeto con data extraida
		data_extraida_comuna['region'] = id_region

		insert_data(url_api_2,data_extraida_comuna)

		time.sleep(1)
		
	try:
		myElem = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, 'bt')))
		browser.execute_script("bp(26834)")

	except TimeoutException:
		print("Se vencio el timeout")

	except Exception:
		browser.close()

	print('Terminando extracción...\n')
	browser.close()


def main():
	
	#Numeros de regiones para URL
	numeros_regiones = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16']

	for n_region in numeros_regiones:
		url = f'http://resultados.censo2017.cl/Region?R=R{n_region}'
		get_data_from_web(url, n_region)


start_time = time.time()	
main()
print("--- %s seconds ---" % (time.time() - start_time))