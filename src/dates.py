#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Get last n days
from datetime import datetime, timedelta

def get_days(n):
    # Get today's date
    today = datetime.now()
    
    # Generate the list of the last n days as datetime objects
    dates = [today - timedelta(days=i) for i in range(n)]
    
    # Sort the list of datetime objects from the oldest to the newest
    sorted_dates = sorted(dates)
    
    # Convert the sorted datetime objects to the desired string format
    sorted_dates_str = [date.strftime('%d/%m/%Y') for date in sorted_dates]
    
    return sorted_dates_str
    
#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Date selector

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_date(driver, date_picker_id, date_str):
    
    # Break down the date and time from the input string
    date, time_str = date_str.split()
    day, month, year = map(int, date.split('/'))
    hour, minute, second = map(int, time_str.split(':'))
    
    # Build the IDs based on the date_picker_id
    date_picker_base_id = "_".join(date_picker_id.split("_")[:-1])
    date_picker_button_id = f"{date_picker_base_id}_B-1"
    calendar_id = f"{date_picker_base_id}_DDD_PWC-1"
    calendar_title_id = f"{date_picker_base_id}_DDD_C_T"
    prev_month_button_id = f"{date_picker_base_id}_DDD_C_PMC"
    next_month_button_id = f"{date_picker_base_id}_DDD_C_NMC"
    day_cell_selector = f"#{date_picker_base_id}_DDD_C_mt td.dxeCalendarDay_Office2010Blue"

    #--- Click the calendar dropdown
    date_picker_button = driver.find_element(By.ID, date_picker_button_id)
    date_picker_button.click()
    
    # Wait for the calendar to become visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, calendar_id))
    )
    
    #--- Navigate to the desired month and year
    while True:
        displayed_month_year = driver.find_element(By.ID, calendar_title_id).text
        displayed_month, displayed_year = displayed_month_year.split(' de ')
        displayed_month = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }[displayed_month]
        displayed_year = int(displayed_year)

        # Move back and forth using the calendar arrows
        if displayed_year == year and displayed_month == month:
            break
        
        if displayed_year > year or (displayed_year == year and displayed_month > month):
            prev_month_button = driver.find_element(By.ID, prev_month_button_id)
            prev_month_button.click()
        else:
            next_month_button = driver.find_element(By.ID, next_month_button_id)
            next_month_button.click()
        
        time.sleep(1)  # Add a pause to allow the calendar to load

    #--- Click the desired day
    # Get all the days of the month  
    day_cells = driver.find_elements(By.CSS_SELECTOR, day_cell_selector) 
    # Count how many times str(day) appears in day_cells
    day_count = [cell.text for cell in day_cells].count(str(day))
    # Initialize a counter for matches
    match_count = 0
    # Select the day at the calendar
    for cell in day_cells:
        if cell.text == str(day):
            match_count += 1
            # If it appears only once, click on it
            if day_count == 1:
                cell.click()
                break
            # If it appears more than once, follow the conditions based on the value of day
            elif day_count > 1:
                # For day <=15, click on the first occurrence
                if day <= 15 and match_count == 1:
                    cell.click()
                    break
                # For day > 15, click on the second occurrence
                elif day > 15 and match_count == 2:
                    cell.click()
                    break