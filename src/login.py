#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Login KINEO

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def login(driver, url, username, password):
    # Navigate to the specified URL
    driver.get(url)
    
    # Wait until the username field is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "LbLogin_I"))
    )
    
    # Enter the username in the username field
    driver.find_element(By.ID, "LbLogin_I").send_keys(username)
    
    # Enter the password in the password field
    driver.find_element(By.ID, "LbPassword_I").send_keys(password)
    
    # Wait for 2 seconds
    sleep(2)
    
    # Wait until the accept button is present
    accept_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ButtonAceptar_I"))
    )
    
    # Scroll the page until the accept button is in view
    driver.execute_script("arguments[0].scrollIntoView();", accept_button)
    
    # Move to the accept button and click it
    ActionChains(driver).move_to_element(accept_button).click().perform()
    
    # Wait until the next page's container is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_ASPxImageLogo"))
    )
    
    # Wait for 1 second
    sleep(1)
