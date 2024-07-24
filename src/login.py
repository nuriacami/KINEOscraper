#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Login KINEO

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "LbLogin_I"))
    )
    driver.find_element(By.ID, "LbLogin_I").send_keys(username)
    driver.find_element(By.ID, "LbPassword_I").send_keys(password)
    sleep(2)
    accept_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ButtonAceptar_I"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", accept_button)
    ActionChains(driver).move_to_element(accept_button).click().perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderDatos_PanelContainer"))
    )
    sleep(2)

