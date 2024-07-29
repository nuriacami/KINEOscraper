from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Click button

def click_button(driver, button_id):
    # Wait until the element is present
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, button_id))
    )

    # Scroll to the element to ensure it is visible
    driver.execute_script("arguments[0].scrollIntoView();", button)

    # Use ActionChains to move to the element and click it
    ActionChains(driver).move_to_element(button).click().perform()

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Click button to download Excel

def download_excel(driver, button_id):
    try:
        # Wait until the element is present
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, button_id))
        )

        # Scroll to the element to ensure it is visible
        driver.execute_script("arguments[0].scrollIntoView();", button)

        # Scroll to the top of the page
        driver.execute_script("window.scrollTo(0, 0);")
        
        # Use ActionChains to move to the element and click it
        ActionChains(driver).move_to_element(button).click().perform()
    except Exception as e:
        print(f"Could not click the button: {e}")