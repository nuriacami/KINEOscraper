#!/usr/bin/env python
# coding: utf-8

# # 1. Setup Driver

# In[2]:


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

# go to "Informe por horas"
driver.get('https://aforadores.mitma.es/contadorestraficofomento/InformePorHorasCalzadaCarrilAforo.aspx')


# # 3. Make the requests and download data

# ### AP7 BARCELONA SECTOR 4

# In[7]:


from src.download import download_week

download_week(driver,
              demarcacion = "AP7 BARCELONA SECTOR 4",
              etd = ['AP7-125+650-100270000000', 'AP7-129+500-100280000000', 'AP7-134+050-100290000000'])


# ### AP7 BARCELONA SECTOR 5

# In[9]:


download_week(driver,
              demarcacion = "AP7 BARCELONA SECTOR 5",
              etd = ['AP7-173+000-100430000000'])


# Exit driver

# In[11]:


driver.quit()


# # 4. Move files to desired directory

# In[13]:


from src.directory import move_to_directory
from private.config import DOWNLOADS_PATH, L_PATH

move_to_directory(origin = DOWNLOADS_PATH,
                  destination = L_PATH)

