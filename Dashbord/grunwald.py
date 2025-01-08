import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import date, time


st.title("Komunikacja miejska we Wrocławiu")

DATE_COLUMN = 'data_aktualizacji'
DATA_URL = 'https://www.wroclaw.pl/open-data/datastore/dump/17308285-3977-42f7-81b7-fdd168c210a2'

def nrToVehicleType(nr):
    if isinstance(nr, str):
        # In Wrocław, only buses have non numeric characters (ex. bus D).
        if not nr.isnumeric():
            return "Autobus"
        nr = int(nr)
    if nr <= 99:
        return "Tramwaj"
    if nr >= 200 and nr <= 299:
        return "Autobus nocny"
    if nr >= 900:
        return "Autobus strefowy"
    return "Autobus"

def vehicleTypeToColor(vehicleType: str):
    if vehicleType == "Tramwaj":
        return [0, 77, 132]
    if vehicleType == "Autobus":
        return [255, 25, 0]
    if vehicleType == "Autobus strefowy":
        return [255, 191, 0]
    if vehicleType == "Autobus nocny":
        return [139, 0, 0]
                        
def load_data():
    data = pd.read_csv(DATA_URL, storage_options={'User-Agent': 'Mozilla/5.0'})
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)

    # Drop nanoseconds and convert to datetime
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN].apply(lambda x: x[:19]), format="%Y-%m-%d %H:%M:%S")
    data["czas_aktualizacji"] = data[DATE_COLUMN].apply(lambda x: str(time(hour = x.hour, minute=x.minute, second=x.second)))

    data.rename(columns={'ostatnia_pozycja_szerokosc': "latitude",
                        'ostatnia_pozycja_dlugosc': "longitude"}, inplace=True)
    
    data["typ_pojazdu"] = data["nazwa_linii"].apply(nrToVehicleType)
    data["kolor"] = data['typ_pojazdu'].apply(vehicleTypeToColor)
    
    # Filter viable data
    filt = (data[DATE_COLUMN].dt.date == date.today()) & (data["nazwa_linii"].notna()) &\
            (data['latitude'] <= 52) & (data['latitude'] >= 50) &\
            (data['longitude'] <= 18) & (data['longitude'] >= 16)
    return data.loc[filt, ["nazwa_linii", "typ_pojazdu", "latitude", "longitude", "czas_aktualizacji", "kolor"]]



data = load_data()

# if st.sidebar.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

selTram = st.multiselect('Tramwaje', data.loc[data['typ_pojazdu']=="Tramwaj", 'nazwa_linii'].unique())
selBus = st.multiselect('Autobusy', data.loc[data['typ_pojazdu']=="Autobus", 'nazwa_linii'].unique())
selOther = st.multiselect('Pozostałe', data.loc[data['typ_pojazdu'].isin(["Autobus strefowy", "Autobus nocny"]), 'nazwa_linii'].unique())

view_state = pdk.ViewState(
    latitude=data['latitude'].mean(),
    longitude=data['longitude'].mean(),
    zoom=12,
    min_zoom=1,
    max_zoom=20)

layer = pdk.Layer(
    type="ScatterplotLayer",
    data=data[data['nazwa_linii'].isin(selTram+selBus+selOther)],
    get_position="[longitude, latitude]",
    get_fill_color="kolor",
    get_radius=2,
    pickable=True,
    radius_scale=1,
    radius_min_pixels=5,
    radius_max_pixels=500
)

pdk_map = pdk.Deck(
    map_provider='carto',
    map_style='light',
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "{nazwa_linii} ({typ_pojazdu})\nostatnia aktualizacja: {czas_aktualizacji}"}
)

st.pydeck_chart(pdk_map)