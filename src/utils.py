#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Funció per mostrar el temps transcorregut

import time
from datetime import timedelta

def print_elapsed_time():
    elapsed_time = time.time() - start_time
    formatted_time = str(timedelta(seconds = elapsed_time))
    print(f"Temps transcorregut: {formatted_time}")

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Funció per verificar si el missatge "No hay datos para mostrar" està present

from selenium.webdriver.common.by import By

def check_no_data_message(driver):
    try:
        no_data_element = driver.find_element(By.CSS_SELECTOR, 'td.dxgv > div')
        if 'No hay datos para mostrar' in no_data_element.text:
            return True
    except:
        pass
    return False