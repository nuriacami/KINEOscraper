#!/usr/bin/env python
# coding: utf-8

# # 1. Setup Driver

# In[2]:


import sys
sys.path.append("../../")
from src.driver import setup_driver
driver = setup_driver()


# # 2. Access to KINEO - informe por horas 

# In[4]:


from src.login import login
from private.config import USER_KEY, PASS_KEY

# login KINEO
login(driver,
      url = 'https://aforadores.mitma.es/contadorestraficofomento/Login.aspx',
      username = USER_KEY, 
      password = PASS_KEY)


# # 3. Make the requests and download data

# In[ ]:


from src.download import download_week
from input.values import VALUES

for values in VALUES:
    download_week(driver, 
                  demarcacion = values["demarcacion"],
                  etd = values["etd"])


# Exit driver

# In[ ]:


driver.quit()


# # 4. Move files to desired directory

# In[ ]:


from src.directory import move_to_directory
from private.config import DOWNLOADS_PATH, L_PATH

move_to_directory(origin = DOWNLOADS_PATH,
                  destination = L_PATH)

