#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Firefox driver setup (Geckodriver)

import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

def setup_driver():
    # driver's path
    driver_path = os.path.join(os.getcwd(), 'bin', 'geckodriver.exe')

    # configure and initialize a Selenium controller for Firefox
    service = Service(executable_path = driver_path)
    driver = webdriver.Firefox(service = service)

    # maximize window 
    driver.maximize_window()
    
    return driver

