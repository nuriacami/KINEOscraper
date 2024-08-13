#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Given a 'demarcacion' and a list of 'etd', download every "Informe por horas" Excel of the past week

def download_week(driver, demarcacion, etd):

    # go to "Informe por horas"
    driver.get('https://aforadores.mitma.es/contadorestraficofomento/InformePorHorasCalzadaCarrilAforo.aspx')

    from src.dropdown import select_dropdown_value

    # Select 'Demarcacion' value
    select_dropdown_value(driver, 
                      input_id = "ctl00_ContentPlaceHolderDatos_CbDemarcacion_I",
                      dropdown_button_id = "ctl00_ContentPlaceHolderDatos_CbDemarcacion_B-1",
                      value = demarcacion)

    from src.dates import get_week, select_date
    from src.button import click_button, download_excel
    from src.utils import print_elapsed_time, check_no_data_message
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
    from time import sleep
    
    # Get days of the past week
    week = get_week()

    for value_to_select_etd in etd:

        # Select 'ETD' value
        select_dropdown_value(driver,
                              input_id = 'ctl00_ContentPlaceHolderDatos_CbEtd_I',
                              dropdown_button_id = 'ctl00_ContentPlaceHolderDatos_CbEtd_B-1',
                              value = value_to_select_etd)

        sleep(1)

        # For every day
        for i in range(len(week) - 1):

            # Initial/End date selector
            select_date(driver,
                        date_picker_id = 'LbFechaInicio_I',
                        date_str = f'{week[i]} 00:00:00')
            
            select_date(driver,
                        date_picker_id = 'LbFechaFin_I',
                        date_str = f'{week[i + 1]} 00:00:00')
            
            sleep(1)
        
            # Select 'Desglose' value
            select_dropdown_value(driver,
                                  input_id = "ctl00_ContentPlaceHolderDatos_CbDesglose_I",
                                  dropdown_button_id = "ctl00_ContentPlaceHolderDatos_CbDesglose_B-1",
                                  value = "CARRIL")
        
            sleep(1)

            # Scroll to the top of the page
            driver.execute_script("window.scrollTo(0, 0);")

            # Click 'Ver' button
            click_button(driver, 
                         button_id = "ctl00_ContentPlaceHolderDatos_BtVerListado_I")
        
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
                driver.execute_script("document.body.style.transform='scale(0.8)'; document.body.style.transformOrigin='0 0';")
                
                # Click to download Excel button
                download_excel(driver,
                               button_id = "ctl00_ContentPlaceHolderDatos_BtExcel_I") 
                
                sleep(2)  # Wait till download is completed 
                
            else:
                # Print message when the ETD has no data
                print(f"La ETD {value_to_select_etd} no conté dades a la seva taula. No es baixarà cap document Excel.")