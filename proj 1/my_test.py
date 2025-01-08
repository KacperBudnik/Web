from selenium import webdriver
from selenium.webdriver.common.by import By

# Inicjalizacja przeglądarki
driver = webdriver.Chrome()  # Upewnij się, że masz zainstalowany WebDriver dla Chrome

for name in ["Zielona+mila-1999-862", "Skazani+na+Shawshank-1994-1048", "Forrest+Gump-1994-998", "Leon+zawodowiec-1994-671", "Requiem+dla+snu-2000-9136", "Matrix-1999-628", "Milczenie+owiec-1991-1047", "Gladiator-2000-936", "Avatar-2009-299113", "Pulp+Fiction-1994-1039"]:
    driver.get("https://www.filmweb.pl/film/"+ name + "#rates")

    # Czekanie na załadowanie strony (opcjonalne, jeśli strona potrzebuje czasu na załadowanie)
    driver.implicitly_wait(10)

    # Pobieranie elementów z div o klasie 'filmDetailedBar' i data-rate od 1 do 10
    results = []
    for rate in range(1, 11):
        element = driver.find_element(By.CSS_SELECTOR, f"div.filmDetailedBar[data-rate='{rate}']")
        results.append( element.text)
    print(name,":  ", results)

# Zamknięcie przeglądarki
driver.quit()
