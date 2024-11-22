from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json


with open("data.json") as f:
    #tmp=print(f.read())
    dane=json.load(f)

options=Options()
#options.add_argument("--headless")
driver=webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
#url="https://web.usos.pwr.edu.pl/"

driver.get("https://web.usos.pwr.edu.pl/")  
#driver.get("https://www.selenium.dev/selenium/web/web-form.html")

driver.implicitly_wait(0.5)

 # kliknij zaloguj się
driver.find_element(
        by=By.ID, value="layout-cas-bar").shadow_root.find_element( 
        By.CSS_SELECTOR, value="#actions > a").click()
# bo jest w shadow_root

driver.find_element(By.ID, value="username").send_keys(dane["user"])
driver.find_element(By.ID, value="password").send_keys(dane["password"])
sleep(2)
driver.find_element(By.CSS_SELECTOR, value="button.login").click()
sleep(2)
driver.find_element(By.CSS_SELECTOR, value='menu-top-item[name="dla studentów"]').shadow_root.find_element(
    By.CSS_SELECTOR, value="a").click()
sleep(2)
driver.find_element(By.XPATH, "//menu-left/ul/li/ul/li/a[contains(text(), 'oceny')]").click()
sleep(2)
#driver.find_element(By.ID, value="main"
#            ).shadow_root.find_element(By.CSS_SELECTOR, value="menu-left"
#                        ).shadow_root.find_elment(By.)

sleep(5)


#text_box=driver.find_element(by=By.NAME, value="my-text")
#submit_button=driver.find_element(by=By.CSS_SELECTOR, value="button")

#text_box.send_keys(dane["user"])
#sleep(2)
#submit_button.click()
#sleep(2)

driver.quit()

#driver.get("https://google.com")

