#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Firefox driver setup (Geckodriver)

import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from private.config import FIREFOX_PATH

def setup_driver():

    # driver's directory (os.pardir mean "../")
    driver_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    # driver's path
    driver_path = os.path.join(driver_dir, 'bin', 'geckodriver.exe')

    # configure service and options for a Selenium controller for Firefox
    service = Service(executable_path = driver_path)
    options = Options()

    # If FIREFOX_PATH is defined, use it; otherwise, let Selenium find the binary automatically
    if os.path.exists(FIREFOX_PATH):
        options.binary_location = FIREFOX_PATH

    # set driver
    driver = webdriver.Firefox(service = service, options = options)

    # maximize window 
    driver.maximize_window()

    return driver
