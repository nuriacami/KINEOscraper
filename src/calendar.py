#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Seleccionar data al selector

def select_date(driver, date_picker_id, date_str):
    
    # Desglossar la data i l'hora del string d'entrada
    date, time_str = date_str.split()
    day, month, year = map(int, date.split('/'))
    hour, minute, second = map(int, time_str.split(':'))
    
    # Construir els IDs basats en el date_picker_id
    date_picker_base_id = "_".join(date_picker_id.split("_")[:-1])
    date_picker_button_id = f"{date_picker_base_id}_B-1"
    calendar_id = f"{date_picker_base_id}_DDD_PWC-1"
    calendar_title_id = f"{date_picker_base_id}_DDD_C_T"
    prev_month_button_id = f"{date_picker_base_id}_DDD_C_PMC"
    next_month_button_id = f"{date_picker_base_id}_DDD_C_NMC"
    day_cell_selector = f"#{date_picker_base_id}_DDD_C_mt td.dxeCalendarDay_Office2010Blue"
    accept_button_xpath = "//button[text()='Aceptar']"

    # Clica al desplegable del calendari
    date_picker_button = driver.find_element(By.ID, date_picker_button_id)
    date_picker_button.click()
    
    # Espera a què el calendari sigui visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, calendar_id))
    )
    
    # Navega fins al mes de l'any desitjat
    while True:
        displayed_month_year = driver.find_element(By.ID, calendar_title_id).text
        displayed_month, displayed_year = displayed_month_year.split(' de ')
        displayed_month = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }[displayed_month]
        displayed_year = int(displayed_year)

        # Es mou amunt i avall amb les fletxes del calendari
        if displayed_year == year and displayed_month == month:
            break
        
        if displayed_year > year or (displayed_year == year and displayed_month > month):
            prev_month_button = driver.find_element(By.ID, prev_month_button_id)
            prev_month_button.click()
        else:
            next_month_button = driver.find_element(By.ID, next_month_button_id)
            next_month_button.click()
        
        time.sleep(1)  # Afegim una pausa per donar temps a la càrrega del calendari

    # Selecciona el dia del mes  
    day_cells = driver.find_elements(By.CSS_SELECTOR, day_cell_selector)
    # Inicialitzem un comptador per a les coincidències
    match_count = 0
    for cell in day_cells:
        if cell.text == str(day):
            match_count += 1  # Incrementem el comptador cada cop que trobem una coincidència
            if day <= 15 or match_count == 2: # Si 'day' és menor o igual a 15, o si hem trobat la segona coincidència
                cell.click()
                break
    
    # Configura el rellotge de les hores, minuts i segons
    time_picker = driver.find_element(By.ID, date_picker_id)
    time_picker.click()
    time_picker.send_keys(Keys.CONTROL + "a")
    time_picker.send_keys(Keys.BACKSPACE)
    time_picker.send_keys(f"{hour:02d}:{minute:02d}:{second:02d}")

    # Confirma la selecció de data mitjançant JavaScript per assegurar-se que es pot fer clic al botó
    accept_button = driver.find_element(By.XPATH, accept_button_xpath)
    driver.execute_script("arguments[0].click();", accept_button)