# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 00:59:20 2016

@author: OriolAndres


Note: Selenium-Firefox issues a prompt each time a .asp file is downloaded for confirmation. 
Changing 'browser.helperApps.neverAsk.saveToDisk' profile option didn't make effect.

"""

import os
import shutil
import time
from selenium import webdriver
from re import sub
from links import links
from news_risk.settings import chromedriver, download_dir


from news_risk.settings import rootdir
datadir = os.path.join(rootdir,'stocks','data')


def fetch_folder():

    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()

    
    chrome_options.add_experimental_option("prefs",{"profile.default_content_settings.popups": 0,
                                                    "download.default_directory":download_dir, 
                                                    "safebrowsing.enabled": "true"})
    os.environ["webdriver.chrome.driver"] = chromedriver    
    driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
    for j,link in enumerate(links):
        if link.startswith('funesp') or link.startswith('lar-es') or link.startswith('prim-') or link.startswith('mediaset'): ## seems to not be working, the enye, must be done manual
            continue
        link = sub('portada','historico',link)
        url = 'http://www.invertia.com/mercados/bolsa/empresas/' + link
        driver.get(url)
        
        
        attempt =0
        while 1:
            try:
                company = driver.find_element_by_xpath("//div[@class='cab_secch1']").text
                com_name, ticker = company.split('\n')
                download = driver.find_element_by_xpath("//a[@class='descargar_excel_red']")
            except Exception as e:
                attempt +=1
                time.sleep(10)
                if attempt > 6: 
                    raise e
            else:
                break
                    
        download.click()
        
        it = 0
        s = 0
        while 1:
            it+=1
            time.sleep(1)
            zname = 'excel.asp'
            clean_name  = sub('[^\d\w\+]','_',com_name)
            if zname in os.listdir(download_dir):
                ns = os.path.getsize(os.path.join(download_dir,zname))
                if ns == s and ns > 0:
                    shutil.move(os.path.join(download_dir,zname), os.path.join(datadir,clean_name + '.asp'))
                    break
                else:
                    s = ns
                    
    driver.quit()
if __name__ == '__main__':
    fetch_folder()