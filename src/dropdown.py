#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Seleccionar valor del menú desplegable

def select_dropdown_value(driver, input_id, dropdown_button_id, value):
    
    # Trobar i fer clic a la fletxa per desplegar el menú
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, dropdown_button_id))
    )
    dropdown_button.click()

    # Esperar que les opcions estiguin disponibles i seleccionar el valor
    options_xpath = f"//td[contains(@class, 'dxeListBoxItem') and text()='{value}']"
    
    try:
        option_to_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, options_xpath))
        )
        
        # Assegurar-se que l'element és dins del viewport abans de fer clic
        driver.execute_script("arguments[0].scrollIntoView(true);", option_to_select)        
        ActionChains(driver).move_to_element(option_to_select).click().perform()

        sleep(1) # necessari perquè el valor estigui visible

        print(f"Valor seleccionat: {value}\n")

    except TimeoutException:
        print(f"TimeoutException: No es pot trobar l'opció amb el valor {value} en el menú desplegable.")

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Obtenir totes les opcions d'un menú desplegable

def get_dropdown_values(driver, dropdown_button_id):
    # Trobar i fer clic a la fletxa per desplegar el menú
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, dropdown_button_id))
    )
    dropdown_button.click()

    options_xpath = "//td[contains(@class, 'dxeListBoxItem')]"
    options_container_xpath = "//div[@id='ctl00_ContentPlaceHolderDatos_CbEtd_DDD_L_D']"

    # Esperar que les opcions estiguin disponibles
    options_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, options_container_xpath))
    )

    # Crear un conjunt per emmagatzemar totes les opcions trobades
    options_set = set()

    # Desplaçar-se i recollir opcions fins que no hi hagi més noves opcions
    last_height = driver.execute_script("return arguments[0].scrollHeight", options_container)
    while True:
        # Recollir les opcions visibles actuals
        options_elements = driver.find_elements(By.XPATH, options_xpath)
        for option in options_elements:
            text = option.text.strip()
            if text != '':
                options_set.add(text)

        # Desplaçar-se fins al final del contenidor per carregar noves opcions
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", options_container)
        time.sleep(1)  # Esperar un moment per donar temps a carregar noves opcions

        # Tornar a llegir les opcions visibles actuals després del scroll
        options_elements = driver.find_elements(By.XPATH, options_xpath)
        for option in options_elements:
            text = option.text.strip()
            if text != '':
                options_set.add(text)

        new_height = driver.execute_script("return arguments[0].scrollHeight", options_container)
        if new_height == last_height:
            break  # Si no es carrega cap nova opció, sortir del bucle
        last_height = new_height

    # Tancar el desplegable fent clic fora de l'àrea del desplegable
    dropdown_button.click()
    time.sleep(1)  # Esperar un moment per assegurar-se que el desplegable es tanca

    # Convertir el conjunt a llista i ordenar-lo per assegurar un ordre consistent
    options = sorted(list(options_set))
    return options
