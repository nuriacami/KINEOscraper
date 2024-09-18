#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Firefox driver setup (Geckodriver)

import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def setup_driver():

    # driver's directory
    driver_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))

    # driver's path
    driver_path = os.path.join(driver_dir, 'bin', 'geckodriver.exe')

    # configure service and options for a Selenium controller for Firefox
    service = Service(executable_path = driver_path)
    # Opcions per configurar el Firefox

    firefox_profile = webdriver.FirefoxProfile()

    # Aquí especifiquem que volem baixar els fitxers automàticament sense preguntar
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  # Tipus de MIME dels fitxers que vols baixar

    options = Options()
    options.profile = firefox_profile

    driver = webdriver.Firefox(service = service)#, options = options)

    # maximize window 
    driver.maximize_window()

    return driver
