#!/usr/bin/env python
# coding: utf-8

# # 1. Setup Driver

# In[1]:


import sys
sys.path.append("../../")
from src.driver import setup_driver
driver = setup_driver()


# # 2. Access to KINEO - informe por horas 

# In[2]:


from src.login import login
from private.config import USER_KEY, PASS_KEY

# login KINEO
login(driver,
      url = 'https://aforadores.mitma.es/contadorestraficofomento/Login.aspx',
      username = USER_KEY, 
      password = PASS_KEY)


# In[3]:


# from src.dropdown import get_all_combinations
# driver.get('https://aforadores.mitma.es/contadorestraficofomento/InformePorHorasCalzadaCarrilAforo.aspx')
# get_all_combinations(driver, 'ctl00_ContentPlaceHolderDatos_CbDemarcacion_B-1', 'ctl00_ContentPlaceHolderDatos_CbEtd_B-1', '../../input/values.py')


# # 3. Make the requests and download data

# In[4]:


from src.download import download_data
from input.values import VALUES

for values in VALUES:
    download_data(driver,
                  demarcacion = values["demarcacion"],
                  etd = values["etd"],
                  option = 'day'
                 )

# calculo que en total triga uns 40min


# Exit driver

# In[ ]:


driver.quit()


# # 4. Move files to desired directory

# In[ ]:


from src.directory import move_to_directory
from private.config import DOWNLOADS_PATH, L_PATH

move_to_directory(origin = DOWNLOADS_PATH,
                  destination = L_PATH)

