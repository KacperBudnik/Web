# creat venv
# pip instal shiny
#shiny create

import pandas as pd

bus_url = "https://www.wroclaw.pl/open-data/datastore/dump/17308285-3977-42f7-81b7-fdd168c210a2"
bus = pd.read_csv(bus_url,  storage_options = {'User-Agent': 'Mozilla/5.0'})

data=bus[["Ostatnia_Pozycja_Szerokosc", "Ostatnia_Pozycja_Dlugosc"]]

data.rename(columns={"Ostatnia_Pozycja_Szerokosc":"sz", "Ostatnia_Pozycja_Dlugosc":"dl"}, inplace=True)

data.dropna()

data[(17.2>data["dl"]) & (data["dl"]>16.8) & (51.2>data["sz"])&(data["sz"]>50.8) ]


















