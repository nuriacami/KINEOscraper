#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Setup driver de Mozilla (Geckodriver)

import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

def setup_driver():
    driver_path = os.path.join(os.getcwd(), 'bin', 'geckodriver.exe')
    service = Service(executable_path = driver_path)
    driver = webdriver.Firefox(service = service)
    driver.maximize_window()
    return driver