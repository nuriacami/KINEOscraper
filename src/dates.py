#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Set [fecha_inicio, fecha_fin] from download_data as the unique date interval

from datetime import datetime, timedelta

def get_days(start_date, end_date):

    # Parse the input dates and convert to the desired format
    start = datetime.strptime(start_date, "%d/%m/%Y").strftime('%d/%m/%Y 00:00:00')
    end = datetime.strptime(end_date, "%d/%m/%Y").strftime('%d/%m/%Y 00:00:00')

    # Convert to vector
    dates = [start, end]

    return dates

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Get days by hours between two dates

def get_hours_between(start_date, end_date):

    # Parse the input dates
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    
    # Include the 00:00:00 of the day after the end_date
    end = end + timedelta(days=1)

    # Generate the hourly timestamps
    hours = []
    current_time = start
    while current_time <= end:
        hours.append(current_time.strftime("%d/%m/%Y %H:%M:%S"))
        current_time += timedelta(hours=1)

    return hours

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Get days between two dates

def get_days_between(start_date, end_date):

    # Increment one day end_date
    end_date = datetime.strptime(end_date, '%d/%m/%Y') + timedelta(days=1)
    end_date = end_date.strftime('%d/%m/%Y')

    # Convert the dates passed as strings to datetime objects
    start = datetime.strptime(start_date, '%d/%m/%Y')
    end = datetime.strptime(end_date, '%d/%m/%Y')
    
    # Ensure the start date is the earlier date
    if start > end:
        start, end = end, start
    
    # Generate the list of dates between the given start and end dates, inclusive
    num_days = (end - start).days
    dates = [start + timedelta(days=i) for i in range(num_days + 1)]
    
    # Convert the datetime objects to the desired format
    dates_str = [date.strftime('%d/%m/%Y 00:00:00') for date in dates]

    return dates_str
    
#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Get months between two dates

def get_months_between(start_date, end_date, n=1):
    # Convert the dates passed as strings to datetime objects
    start = datetime.strptime(start_date, '%d/%m/%Y')
    end = datetime.strptime(end_date, '%d/%m/%Y')

    # Ensure the start date is earlier or equal to the end date
    if start > end:
        start, end = end, start

    # Generate the list of months with the specified interval
    months = []
    current = start.replace(day=1)
    while current <= end:
        months.append(current.strftime('%d/%m/%Y 00:00:00'))
        # Move to the next month with the specified interval
        next_month = (current.month - 1 + n) % 12 + 1
        next_year = current.year + (current.month - 1 + n) // 12
        current = current.replace(year=next_year, month=next_month)

    return months

#------------------------------------------------------------------------------------------------------------------------------------------------------#
######## Date selector

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_date(driver, date_picker_id, date_str, choice='por_horas'):
    
    # Break down the date and time from the input string
    date, time_str = date_str.split()
    day, month, year = map(int, date.split('/'))
    hour, minute, second = map(int, time_str.split(':'))
    
    # Build the IDs based on the date_picker_id
    date_picker_base_id = "_".join(date_picker_id.split("_")[:-1])
    date_picker_button_id = f"{date_picker_base_id}_B-1"
    calendar_id = f"{date_picker_base_id}_DDD_PW-1"
    calendar_title_id = f"{date_picker_base_id}_DDD_C_T"
    prev_month_button_id = f"{date_picker_base_id}_DDD_C_PMC"
    next_month_button_id = f"{date_picker_base_id}_DDD_C_NMC"
    prev_year_button_id = f"{date_picker_base_id}_DDD_C_PYC"
    next_year_button_id = f"{date_picker_base_id}_DDD_C_NYC"
    day_cell_selector = f"#{date_picker_base_id}_DDD_C_mt td.dxeCalendarDay_Office2010Blue"
    time_input_id = f"{date_picker_base_id}_DDD_C_TE_I"
    increment_button_id = f"{date_picker_base_id}_DDD_C_TE_B-2"
    decrement_button_id = f"{date_picker_base_id}_DDD_C_TE_B-3"
    accept_button_id = f"{date_picker_base_id}_DDD_C_BO"

    #--- Click the calendar dropdown
    date_picker_button = driver.find_element(By.ID, date_picker_button_id)
    date_picker_button.click()
    
    # Wait for the calendar to become visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, calendar_id))
    )
    
    #--- Navigate to the desired month and year
    max_attempts = 5  # Maximum number of attempts to wait for the text
    attempt = 0
    last_valid_month_year = None

    while True:
        # Try to get the value of the month/year with a maximum number of attempts
        while attempt < max_attempts:
            displayed_month_year = driver.find_element(By.ID, calendar_title_id).text
            if displayed_month_year.strip():  # Check that the text is not empty
                last_valid_month_year = displayed_month_year  # Update the last valid value
                break
            time.sleep(1)  # Wait before trying again
            attempt += 1

        # If after the attempts the text is still empty, use the last valid value
        if not displayed_month_year.strip():
            if last_valid_month_year is not None:
                displayed_month_year = last_valid_month_year
            else:
                raise ValueError("Could not find a valid value for the calendar title.")

        # Now that we have a valid text, proceed with the split
        displayed_month, displayed_year = displayed_month_year.split(' de ')
        displayed_month = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }[displayed_month]
        displayed_year = int(displayed_year)

        # Check if we are already at the desired month and year
        if displayed_year == year and displayed_month == month:
            break

        # Calculate the difference in years and months
        year_diff = year - displayed_year
        month_diff = month - displayed_month + (year_diff * 12)

        # Decide the optimal movement
        if abs(year_diff) > 1 or (abs(year_diff) == 1 and abs(month_diff) > 6):
            # Move by years if there's more than one year difference or it's shorter
            if year_diff > 0:
                next_year_button = driver.find_element(By.ID, next_year_button_id)
                next_year_button.click()
            else:
                prev_year_button = driver.find_element(By.ID, prev_year_button_id)
                prev_year_button.click()
        elif abs(month_diff) > 0:
            # Move by months when the difference is less than a year
            if month_diff > 0:
                next_month_button = driver.find_element(By.ID, next_month_button_id)
                next_month_button.click()
            else:
                prev_month_button = driver.find_element(By.ID, prev_month_button_id)
                prev_month_button.click()
        else:
            raise ValueError("Unknown error in calendar movement.")

        time.sleep(0.2)  ## Small delay to allow UI to update

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
                # For day <= 15, click on the first occurrence
                if day <= 15 and match_count == 1:
                    cell.click()
                    break
                # For day > 15, click on the second occurrence
                elif day > 15 and match_count == 2:
                    cell.click()
                    break

    if choice == 'por_minutos':
        # --- Set the hour in the time input
        # Get the current hour value
        time_input = driver.find_element(By.ID, time_input_id)
        current_hour = int(time_input.get_attribute("value").split(':')[0])  # Extract the hour part

        # Calculate the shortest path to the desired hour
        forward_steps = (hour - current_hour) % 24
        backward_steps = (current_hour - hour) % 24

        if forward_steps < backward_steps:
            clicks = forward_steps
            button_id = increment_button_id
        else:
            clicks = backward_steps
            button_id = decrement_button_id

        # Perform the clicks
        for _ in range(clicks):
            button = driver.find_element(By.ID, button_id)
            button.click()
            time.sleep(0.2)  # Small delay to allow UI to update

        # --- Click 'Acceptar' button to close the calendar
        from src.button import click_button
        click_button(driver, button_id=accept_button_id)


###################################################################### DEPRACATED ###################################################################### 

# #------------------------------------------------------------------------------------------------------------------------------------------------------#
# ######## Get last n days by hours

# from datetime import datetime, timedelta

# def get_last_hours(n):
#     # Today's date at 00:00
#     today = datetime.now()
#     today_00 = datetime(today.year, today.month, today.day)

#     # Calculate the starting point: `n` days before today
#     start_time = today_00 - timedelta(days=n)

#     # Generate a list of hours from `start_time` to `today_00 + 1 hour`
#     hours = []
#     current_time = start_time
#     while current_time <= today_00:
#         hours.append(current_time.strftime("%d/%m/%Y %H:%M:%S"))
#         current_time += timedelta(hours=1)

#     return hours

# #------------------------------------------------------------------------------------------------------------------------------------------------------#
# ######## Get last n days

# def get_last_days(n):

#     # Increment number of days in 1
#     n = n + 1 

#     # Get today's date
#     today = datetime.now()
    
#     # Generate the list of the last n days as datetime objects
#     dates = [today - timedelta(days=i) for i in range(n)]
    
#     # Sort the list of datetime objects from the oldest to the newest
#     sorted_dates = sorted(dates)

#     # Convert the sorted datetime objects to the desired string format
#     sorted_dates_str = [date.strftime('%d/%m/%Y 00:00:00') for date in sorted_dates]

#     return sorted_dates_str