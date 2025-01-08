from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#import json
import numpy as np
#from numpy import array
#from numpy import sum as np.sum

with open("valid-wordle-words.txt", "r")  as file:
    tmp = file.read().split("\n")[1:-1] # ostatni jest pusty
    
words = np.array([list(x) for x in tmp]) # macierz słów -- wiersze = słowa, i-ta kolumna = wektor i-tych liter


options=Options()
#options.add_argument("--headless")
driver=webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
#url="https://web.usos.pwr.edu.pl/"

driver.get("https://www.nytimes.com/games/wordle/index.html")  
#driver.get("https://www.selenium.dev/selenium/web/web-form.html")

driver.implicitly_wait(0.5)

sleep(4)
driver.find_element(    
        By.CSS_SELECTOR, value='button.fides-banner-button.fides-banner-button-primary.fides-reject-all-button').click() # Reject cookies
sleep(1)
driver.find_element(    
        By.CSS_SELECTOR, value='.purr-blocker-card__button').click() 
sleep(2)
driver.find_element(    
        By.CSS_SELECTOR, value='button[data-testid="Play"]').click() # Play
sleep(1)
driver.find_element(
        By.CSS_SELECTOR, value="button.Modal-module_closeIcon__TcEKb").click() # Close instruction


def write(word):
    for letter in word:
        driver.find_element(
            By.CSS_SELECTOR, value='button[data-key="' + letter.lower() +'"]').click()
        sleep(0.3)
    driver.find_element(
            By.CSS_SELECTOR, value='button[data-key="↵"]').click()
    sleep(2) # Czekanie na koniec animacji
    
def get_result(i):
    res=np.array([])
    for j in range(1,6):
        css='div[aria-label="Row '+str(i)+'"] > div:nth-child('+str(j)+') > div'
        txt=driver.find_element(
                By.CSS_SELECTOR, value=css).get_attribute("aria-label").split()
        #print(txt)
        if txt[-1]=="absent":
            res = np.append(res, -1)
        elif txt[-1]=="position":
            res = np.append(res, 0)
        elif txt[-1]=="correct":
            res = np.append(res, 1)
        else:
            res.append(123)
    return res
     
    
possible=np.ones(len(words), dtype=bool)
win=False

for i in range(1,7):
    print("W kroku " + str(i) + " zgaduję spośród: " + str(sum(possible==1)) + " słów!")
    choosen_id = np.random.choice(np.where(possible)[0])
    choosen_word="".join(words[choosen_id,:])    
    write(choosen_word)
    matched=get_result(i)
    if all(matched==1):
        win=True
        break
    possible[choosen_id] == False
    for j in range(0,5):
        if matched[j]==-1:
            if np.all(matched[words[choosen_id,:]==choosen_word[j]]==-1): # że wszystkie dane literki są szare
                possible &= np.all( (words != choosen_word[j]), axis=1) 
        elif matched[j]==1:
            possible &= words[:,j] == choosen_word[j]
        elif matched[j]==0:
             possible &= np.any( (words == choosen_word[j]), axis=1) & (words[:,j] != choosen_word[j])
    sleep(1)

if win:
    print("Gratulacje dla mnie!")
else:
    print("Przegrana... \nPozostało " + str(sum(possible==1)) + " możliwych słów.")
    if sum(possible==1) <30:
        print("Są to:")
        for word in words[possible]:
            print("".join(word))
sleep(5)

driver.quit()






