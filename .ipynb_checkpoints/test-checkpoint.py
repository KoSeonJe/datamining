import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
url = "https://www.imdb.com/title/tt13918776/?ref_=fn_al_tt_1"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
time.sleep(1)
temps = soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > div.sc-92625f35-10.dwKwMe > section > div.ipc-chip-list--baseAlt.ipc-chip-list > div.ipc-chip-list__scroller > a:nth-child(1)')
# document.querySelector("#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-978e9339-1.ihWZgK.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(28) > div.sc-f5ef05d0-0.gutvDK > ul.ipc-metadata-list.ipc-metadata-list--dividers-all.sc-f5ef05d0-1.WmMVu.ipc-metadata-list--base > li:nth-child(2) > div > ul > li > span")
print(temps)

 #__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-978e9339-1.ihWZgK.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(28) > div.ipc-title.ipc-title--base.ipc-title--section-title.ipc-title--on-textPrimary > div > hgroup > h3 > span
 #__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-978e9339-1.ihWZgK.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(32) > div.ipc-title.ipc-title--base.ipc-title--section-title.ipc-title--on-textPrimary > div > hgroup > h3 > span
