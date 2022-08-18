__version__ = '0.1'
__author__ = 'Jose Miguel Chávez'

import json
import logging
from typing import Dict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import time

def _parseInt(value: str):
	return int(value.replace('.',''))

def _parseFloat(value: str):
	value = value.replace(',','.')
	return float(value.replace('%',''))

def _getDataFromBrowser(browser: webdriver):
    population = _parseInt(browser.find_element_by_xpath('.//*[@id="valorpoblacion"]').text)
    number_households = _parseInt(browser.find_element_by_xpath('.//*[@id="valirvivienda"]').text)
    men_population = _parseInt(browser.find_element_by_xpath('.//*[@id="valorhombres"]').text)
    women_population = _parseInt(browser.find_element_by_xpath('.//*[@id="valoresmujer"]').text)
    population_density = _parseFloat(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[1]/div/table/tbody/tr[1]/td[2]').text)
    migrant_population = _parseInt(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[4]/div/table/tbody/tr[1]/td[2]').text)
    migrant_population_percent = _parseFloat(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[4]/div/table/tbody/tr[4]/td[2]').text)
    native_population_percent = _parseFloat(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[1]/div/table/tbody/tr[7]/td[2]').text)
    women_employment_percent = _parseFloat(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[6]/div/table/tbody/tr[3]/td[2]').text)
    overcrowding_percent = _parseFloat(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[2]/div/table/tbody/tr[2]/td[2]').text)
    number_homes = _parseInt(browser.find_element_by_xpath(
        './html/body/div/div[2]/div[1]/div[2]/div[3]/div/table/tbody/tr[1]/td[2]').text)

    return {
		'population': population,
		'number_households': number_households,
		'men_population': men_population,
		'women_population': women_population,
		'population_density': population_density,
		'migrant_population': migrant_population,
		'migrant_population_percent': migrant_population_percent,
		'native_population_percent': native_population_percent,
		'women_employment_percent': women_employment_percent,
		'overcrowding_percent': overcrowding_percent,
		'number_homes': number_homes,
	}

def _getRegionData(n_region: str) -> Dict:
    browser = webdriver.Chrome(ChromeDriverManager().install())
    url = f'http://resultados.censo2017.cl/Region?R=R{n_region}'

    print("Starting browser")
    print(url)
    browser.get(url)

    region = browser.find_element_by_xpath('.//*[@id="nombreregion"]').text
    region_data = _getDataFromBrowser(browser)

    comunas_select = browser.find_element_by_xpath('.//*[@id="comobocomunas"]')
    comunas_select_object = Select(comunas_select)
    comunas_select_options = comunas_select_object.options

    comunas_data = []
    for i, comuna_option in enumerate(comunas_select_options):
        comunas_select_object.select_by_index(i)
        comuna_id = int(comuna_option.get_attribute('value'))
        if comuna_id != 0:
            comuna = str(browser.find_element_by_xpath('.//*[@id="nombrecomuna"]').text)[6:].strip().lower()
            comuna_data = _getDataFromBrowser(browser)
            comuna_data['comuna_id'] = comuna_id
            comuna_data['comuna'] = comuna
            comunas_data.append(comuna_data)
        time.sleep(1)

    region_data['region_id'] = int(n_region)
    region_data['region'] = region
    region_data['comunas'] = comunas_data

    try:
        myElem = WebDriverWait(browser,2).until(EC.presence_of_element_located((By.ID, 'bt')))
        browser.execute_script("bp(26834)")
    except TimeoutException:
        logging.debug("Se vencio el timeout")
        # print("Se vencio el timeout")
    except Exception as e:
        browser.close()
        logging.error(str(e))

    print('Closing browser...\n')
    browser.close()

    return region_data

def main():
    n_regions = [
        '01','02','03','04',
        '05','06','07','08',
        '09','10','11','12',
        '13','14','15','16'
    ]

    regions_data = []
    for n_region in n_regions:
        region_data = _getRegionData(n_region)
        regions_data.append(region_data)

    with open('censo-2017.json', 'w', encoding='utf-8') as f:
        json.dump(regions_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()