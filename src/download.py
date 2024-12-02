#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Given a 'demarcacion' and a list of 'etd', download every hour/day Excel 

def download_data(driver, demarcacion, etd, option='por_horas'):

    if option == 'por_minutos':
        # Go to Aforos < Informes < Volumen Tráfico Agrupado
        driver.get('https://aforadores.mitma.es/contadorestraficofomento/InformeVolumenTraficoAgrupadoAforo.aspx')
    elif option == 'por_horas': 
        # Go to Aforos < Informes < Volumen Medio por Horas
        driver.get('https://aforadores.mitma.es/contadorestraficofomento/InformePorHorasCalzadaCarrilAforo.aspx')

    from src.dropdown import select_dropdown_value
    # Select 'Demarcacion' value
    select_dropdown_value(driver, 
                      dropdown_button_id = "ctl00_ContentPlaceHolderDatos_CbDemarcacion_B-1",
                      dropdown_container_id = 'ctl00_ContentPlaceHolderDatos_CbDemarcacion_DDD_L_D',
                      value = demarcacion)

    from src.dates import get_days, get_dates_between, select_date
    from src.button import click_button, download_excel
    from src.utils import print_elapsed_time, check_no_data_message, is_page_blocked
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
    from time import sleep
    import datetime

    # Get dates depending on parameter 'option'
    if option == 'por_minutos':
        start = '01/11/2024' # descarregar un interval concret
        send = '07/11/2024'
        dates = get_hours_between(start, end)
    elif option == 'por_horas':
        # dates = get_days(1) # descarregar 1 dia
        # dates = get_days(7) # descarregar 1 setmana
        # dates = get_days(datetime.datetime.now().timetuple().tm_yday + 1) # descarrgar 1 any sencer
        # dates = get_days(30) # descarregar els últims 30 dies
        # start = '01/09/2024' # descarregar un interval concret
        # end = '30/09/2024'
        # dates = get_days_between(start, end) 

    for value_to_select_etd in etd:

        # Select 'ETD' value
        select_dropdown_value(driver,
                              dropdown_button_id='ctl00_ContentPlaceHolderDatos_CbEtd_B-1',
                              dropdown_container_id='ctl00_ContentPlaceHolderDatos_CbEtd_DDD_L_D',
                              value=value_to_select_etd)

        sleep(1)

        # For every date
        for i in range(len(dates) - 1):

            retry_count = 0
            max_retries = 5  # Set a maximum number of retries to avoid infinite loops

            while retry_count < max_retries:

                try:
                    # Initial/End date selector
                    select_date(driver,
                                date_picker_id='LbFechaInicio_I',
                                date_str=dates[i])

                    select_date(driver,
                                date_picker_id='LbFechaFin_I',
                                date_str=dates[i + 1])

                    sleep(1)

                    if option == 'por_minutos':
                        # Select 'Desglose' value == 5 (MINUTOS)
                        select_dropdown_value(driver,
                                            dropdown_button_id="ctl00_ContentPlaceHolderDatos_CbDesgloseMinutos_B-1",
                                            dropdown_container_id='ctl00_ContentPlaceHolderDatos_CbDesgloseMinutos_DDD_L_D',
                                            value="5")
                    elif option == 'por_horas':
                        # Select 'Desglose' value == CARRIL
                        select_dropdown_value(driver,
                                            dropdown_button_id="ctl00_ContentPlaceHolderDatos_CbDesglose_B-1",
                                            dropdown_container_id='ctl00_ContentPlaceHolderDatos_CbDesglose_DDD_L_D',
                                            value="CARRIL")

                    sleep(1)

                    # Scroll to the top of the page
                    driver.execute_script("window.scrollTo(0, 0);")

                    # Click 'Ver' button
                    click_button(driver,
                                 button_id="ctl00_ContentPlaceHolderDatos_BtVerListado_I")

                    # Wait for "LoadingPanel" to appear
                    sleep(2)

                    # Wait until results table is loaded
                    while True:
                        try:
                            # Check if "LoadingPanel" is visible
                            WebDriverWait(driver, 1).until(
                                EC.visibility_of_element_located((By.ID, "LoadingPanel"))
                            )
                        except TimeoutException:
                            break

                    sleep(2)

                    # While message "No hay datos para mostrar" is not shown, Excel will be downloaded
                    if not check_no_data_message(driver):

                        # Zoom out to 80% in order to make download Excel button visible
                        driver.execute_script(
                            "document.body.style.transform='scale(0.8)'; document.body.style.transformOrigin='0 0';")

                        # Click to download Excel button
                        download_excel(driver,
                                       button_id="ctl00_ContentPlaceHolderDatos_BtExcel_I")

                        sleep(2)  # Wait till download is completed
                        
                        # Exit the retry loop as the download succeeded
                        break

                    else:
                        # Print message when the ETD has no data
                        print(f"La ETD {value_to_select_etd} no conté dades a la seva taula. No es baixarà cap document Excel.")
                        break  # No data, no need to retry

                except Exception as e:
                    if is_page_blocked(driver):
                        print(f"Pàgina bloquejada detectada. Reintentant... (Intent {retry_count + 1})")
                        driver.refresh()  # Refresh the page if blocked
                        sleep(5)  # Allow some time for the page to reload
                        retry_count += 1  # Increment the retry counter
                    else:
                        raise e  # Rethrow the exception if it's not related to the blocked page

            if retry_count == max_retries:
                print(f"No s'ha pogut descarregar l'Excel després de {max_retries} intents.")
