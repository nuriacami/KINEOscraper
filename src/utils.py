#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Displaying elapsed time

import time
from datetime import timedelta

def print_elapsed_time(start_time):
    elapsed_time = time.time() - start_time
    formatted_time = str(timedelta(seconds = elapsed_time))
    print(f"Temps transcorregut: {formatted_time}")

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Verify whether “"No hay datos para mostrar"” message is present

from selenium.webdriver.common.by import By

def check_no_data_message(driver):
    try:
        no_data_element = driver.find_element(By.CSS_SELECTOR, 'td.dxgv > div')
        if 'No hay datos para mostrar' in no_data_element.text:
            return True
    except:
        pass
    return False

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Check for the blocked page

def is_page_blocked(driver):
    try:
        # Detect if the blocked page image is present
        blocked_image = driver.find_element(By.XPATH, "//img[@src='https://mfomseclogoimage.s3.amazonaws.com/LogoMTMS2.png']")
        return blocked_image is not None
    except:
        return False

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Check if the session has expired

from selenium.common.exceptions import NoSuchElementException

def has_session_expired(driver):
    try:
        # Find the element with id 'LbTituloLabel'
        element = driver.find_element(By.ID, "LbTituloLabel")
        # Verify that the text is exactly 'TIEMPO DE SESIÓN EXPIRADO'
        if element.text.strip() == "TIEMPO DE SESIÓN EXPIRADO":
            return True
        return False
    except NoSuchElementException:
        return False
        
#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Checks if the download is complete

import os

def is_download_complete(download_path, initial_file_count):

    while True:
        # Count the files in the download folder
        current_file_count = len(os.listdir(download_path))
        
        # If the file count has increased, assume the download is complete
        if current_file_count > initial_file_count:
            return True

        time.sleep(60)