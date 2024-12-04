from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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

def download_excel_button(driver, button_id):

    from private.config import DOWNLOADS_PATH
    from src.utils import is_download_complete

    try:        
        # Count the number of files in the download folder before the click
        initial_file_count = len(os.listdir(DOWNLOADS_PATH))

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

        # Wait until the download is complete
        is_download_complete(DOWNLOADS_PATH, initial_file_count)

    except Exception as e:
        print(f"Could not click the button: {e}")