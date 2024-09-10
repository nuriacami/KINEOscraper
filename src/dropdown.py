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
######## Get all value combinations from two dropdown menus

def get_all_combinations(driver, demarcacion_dropdown_id, etd_dropdown_id, output_file_path):

    # Get all available options in the 'demarcacion' dropdown
    def get_demarcacion_values():

        # Find and click the arrow to open the dropdown menu
        dropdown_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, demarcacion_dropdown_id))
        )
        dropdown_button.click()

        options_xpath = "//td[contains(@class, 'dxeListBoxItem')]"
        options_container_xpath = "//div[@id='ctl00_ContentPlaceHolderDatos_CbDemarcacion_DDD_L_D']"

        # Wait for the options to be available
        options_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, options_container_xpath))
        )

        # Create a list to store all the found options in order
        demarcacion_values = []

        # Scroll and collect options until no more new options appear
        last_height = driver.execute_script("return arguments[0].scrollHeight", options_container)
        while True:
            # Collect currently visible options
            options_elements = driver.find_elements(By.XPATH, options_xpath)
            for option in options_elements:
                text = option.text.strip()
                if text != '' and text not in demarcacion_values:
                    demarcacion_values.append(text)  # Add to list instead of set to preserve order

            # Scroll to the end of the container to load new options
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", options_container)
            time.sleep(1)  # Wait a moment to allow new options to load

            # Re-read the currently visible options after scrolling
            options_elements = driver.find_elements(By.XPATH, options_xpath)
            for option in options_elements:
                text = option.text.strip()
                if text != '' and text not in demarcacion_values:
                    demarcacion_values.append(text)  # Add to list to preserve order

            new_height = driver.execute_script("return arguments[0].scrollHeight", options_container)
            if new_height == last_height:
                break  # If no new options load, exit the loop
            last_height = new_height

        # Close the dropdown by clicking outside the dropdown area
        dropdown_button.click()
        time.sleep(1)  # Wait a moment to ensure the dropdown closes

        return demarcacion_values  # The list is already in the order of appearance

    # Get all available options in the 'etd' dropdown for a specific 'demarcacion'
    def get_etd_values():
        etd_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, etd_dropdown_id))
        )
        etd_button.click()

        etd_options_xpath = "//td[contains(@class, 'dxeListBoxItem')]"
        options_container_xpath = "//div[@id='ctl00_ContentPlaceHolderDatos_CbEtd_DDD_L_D']"

        etd_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, options_container_xpath))
        )

        # Create a list to store the etd options while maintaining the order
        etd_list = []

        # Scroll and collect options until no more new options appear
        last_height = driver.execute_script("return arguments[0].scrollHeight", etd_container)
        while True:
            # First collection of visible options
            etd_elements = driver.find_elements(By.XPATH, etd_options_xpath)
            for option in etd_elements:
                text = option.text.strip()
                if text != '' and text not in etd_list:  # Ensure no duplicates
                    etd_list.append(text)

            # Scroll to the end of the container to load new options
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", etd_container)
            time.sleep(1)  # Small wait to allow new elements to load

            # Second collection after scrolling
            etd_elements = driver.find_elements(By.XPATH, etd_options_xpath)
            for option in etd_elements:
                text = option.text.strip()
                if text != '' and text not in etd_list:  # Ensure no duplicates
                    etd_list.append(text)

            # Check if new options are loaded by comparing the scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", etd_container)
            if new_height == last_height:
                break
            last_height = new_height

        # Close the dropdown
        etd_button.click()

        return etd_list
    
    def write_to_file(data):
            with open(output_file_path, "a") as f:
                # Add a blank line before writing the vector
                f.write("\n")  
                f.write(f"VALUES = {data}\n")
                
    # Capture all values from the 'demarcacion' dropdown
    demarcacion_values = get_demarcacion_values()

    # List to store the combinations of demarcacion and their corresponding ETD values
    all_combinations = []

    # For each 'demarcacion' value, capture the corresponding 'etd' values
    for demarcacion in demarcacion_values:
        # Select the 'demarcacion' value
        demarcacion_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, demarcacion_dropdown_id))
        )
        demarcacion_button.click()

        demarcacion_option_xpath = f"//td[contains(@class, 'dxeListBoxItem') and text()='{demarcacion}']"
        demarcacion_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, demarcacion_option_xpath))
        )
        demarcacion_option.click()

        # Capture the ETD values for this 'demarcacion'
        etd_values = get_etd_values()

        # Add the combination to the all_combinations list
        all_combinations.append({
            "demarcacion": demarcacion,
            "etd": etd_values
        })

    # Write the contents of the 'all_combinations' list to the file in the correct format
    write_to_file(all_combinations)


# PROPOSTA INICIAL: retorna tots els valors però no ordenats
# # Get all available options in the 'etd' dropdown for a specific 'demarcacion'
#     def get_etd_values():
#         etd_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.ID, etd_dropdown_id))
#         )
#         etd_button.click()

#         etd_options_xpath = "//td[contains(@class, 'dxeListBoxItem')]"
#         options_container_xpath = "//div[@id='ctl00_ContentPlaceHolderDatos_CbEtd_DDD_L_D']"

#         etd_container = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, options_container_xpath))
#         )

#         # Create a set to store all the found etd options
#         etd_set = set()

#         # Scroll and collect options until no more new options appear
#         last_height = driver.execute_script("return arguments[0].scrollHeight", etd_container)
#         while True:
#             # Collect currently visible options
#             etd_elements = driver.find_elements(By.XPATH, etd_options_xpath)
#             for option in etd_elements:
#                 text = option.text.strip()
#                 if text != '':
#                     etd_set.add(text)

#             # Scroll to the end of the container to load new options
#             driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", etd_container)
#             time.sleep(1)

#             # Re-read the currently visible options after scrolling
#             etd_elements = driver.find_elements(By.XPATH, etd_options_xpath)
#             for option in etd_elements:
#                 text = option.text.strip()
#                 if text != '':
#                     etd_set.add(text)

#             new_height = driver.execute_script("return arguments[0].scrollHeight", etd_container)
#             if new_height == last_height:
#                 break
#             last_height = new_height

#         # Close the dropdown
#         etd_button.click()

#         # Convert the set to a list
#         etd_values = list(etd_set)
#         return etd_values

# PROPOSTA CHATGPT: valors ordenats però falten valors           
    # def get_etd_values():
    #     etd_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.ID, etd_dropdown_id))
    #     )
    #     etd_button.click()

    #     etd_options_xpath = "//td[contains(@class, 'dxeListBoxItem')]"
    #     options_container_xpath = "//div[@id='ctl00_ContentPlaceHolderDatos_CbEtd_DDD_L_D']"

    #     etd_container = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, options_container_xpath))
    #     )

    #     # Create a list to store the etd options while maintaining the order
    #     etd_list = []

    #     # Scroll and collect options until no more new options appear
    #     last_height = driver.execute_script("return arguments[0].scrollHeight", etd_container)
    #     while True:
    #         # Collect currently visible options
    #         etd_elements = driver.find_elements(By.XPATH, etd_options_xpath)
    #         for option in etd_elements:
    #             text = option.text.strip()
    #             if text != '' and text not in etd_list:  # Ensure no duplicates
    #                 etd_list.append(text)  # Use append for lists

    #         # Scroll to the end of the container to load new options
    #         driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", etd_container)
    #         time.sleep(1)

    #         new_height = driver.execute_script("return arguments[0].scrollHeight", etd_container)
    #         if new_height == last_height:
    #             break
    #         last_height = new_height

    #     # Close the dropdown
    #     etd_button.click()

    #     return etd_list