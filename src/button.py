from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Clicar botó

def click_button(driver, button_id):
    # Esperar fins que l'element sigui present
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, button_id))
    )

    # Desplaçar-se a l'element per assegurar-se que està visible
    driver.execute_script("arguments[0].scrollIntoView();", button)

    # Utilitzar ActionChains per moure's a l'element i clicar-lo
    ActionChains(driver).move_to_element(button).click().perform()

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Clicar botó per baixar Excel

def download_excel(driver, button_id):
    try:
        # Esperar fins que l'element sigui present
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, button_id))
        )

        # Desplaçar-se a l'element per assegurar-se que està visible
        driver.execute_script("arguments[0].scrollIntoView();", button)

        # Fer scroll fins a dalt de tot de la pàgina
        driver.execute_script("window.scrollTo(0, 0);")
        
        # Utilitzar ActionChains per moure's a l'element i clicar-lo
        ActionChains(driver).move_to_element(button).click().perform()
    except Exception as e:
        print(f"No s'ha pogut clicar el botó: {e}")
