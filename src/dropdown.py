from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from time import sleep

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Select value from dropdown menu

def select_dropdown_value(driver, input_id, dropdown_button_id, value):
    
    # Find and click the arrow to open the dropdown menu
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, dropdown_button_id))
    )
    dropdown_button.click()

    # Wait for the options to be available and select the value
    options_xpath = f"//td[contains(@class, 'dxeListBoxItem') and text()='{value}']"
    
    try:
        option_to_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, options_xpath))
        )
        
        # Ensure the element is in the viewport before clicking
        driver.execute_script("arguments[0].scrollIntoView(true);", option_to_select)        
        ActionChains(driver).move_to_element(option_to_select).click().perform()

        sleep(1) # necessary to make sure the value is visible

    except TimeoutException:
        print(f"TimeoutException: Could not find the option with value {value} in the dropdown menu.")

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Get all options from a dropdown menu

def get_dropdown_values(driver, dropdown_button_id):
    # Find and click the arrow to open the dropdown menu
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, dropdown_button_id))
    )
    dropdown_button.click()

    options_xpath = "//td[contains(@class, 'dxeListBoxItem')]"
    options_container_xpath = "//div[@id='ctl00_ContentPlaceHolderDatos_CbEtd_DDD_L_D']"

    # Wait for the options to be available
    options_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, options_container_xpath))
    )

    # Create a set to store all the found options
    options_set = set()

    # Scroll and collect options until no more new options appear
    last_height = driver.execute_script("return arguments[0].scrollHeight", options_container)
    while True:
        # Collect currently visible options
        options_elements = driver.find_elements(By.XPATH, options_xpath)
        for option in options_elements:
            text = option.text.strip()
            if text != '':
                options_set.add(text)

        # Scroll to the end of the container to load new options
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", options_container)
        time.sleep(1)  # Wait a moment to allow new options to load

        # Re-read the currently visible options after scrolling
        options_elements = driver.find_elements(By.XPATH, options_xpath)
        for option in options_elements:
            text = option.text.strip()
            if text != '':
                options_set.add(text)

        new_height = driver.execute_script("return arguments[0].scrollHeight", options_container)
        if new_height == last_height:
            break  # If no new options load, exit the loop
        last_height = new_height

    # Close the dropdown by clicking outside the dropdown area
    dropdown_button.click()
    time.sleep(1)  # Wait a moment to ensure the dropdown closes

    # Convert the set to a list and sort it to ensure consistent order
    options = sorted(list(options_set))
    return options
