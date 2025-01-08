import pydeck as pdk
import shiny.express
import pandas as pd

@shiny.express.render.ui
def map():
    bus_url = "https://www.wroclaw.pl/open-data/datastore/dump/17308285-3977-42f7-81b7-fdd168c210a2"
    bus = pd.read_csv(bus_url,  storage_options = {'User-Agent': 'Mozilla/5.0'})
    data=bus[["Ostatnia_Pozycja_Szerokosc", "Ostatnia_Pozycja_Dlugosc"]]

    data.rename(columns={"Ostatnia_Pozycja_Szerokosc":"sz", "Ostatnia_Pozycja_Dlugosc":"dl"}, inplace=True)

    data.dropna()

    data=data[(17.2>data["dl"]) & (data["dl"]>16.8) & (51.2>data["sz"])&(data["sz"]>50.8) ]
    print(data)
    layer = pdk.Layer(
        "ScatterplotLayer",  # `type` positional argument is here
        bus,
        get_position=["sz", "dl"],
        auto_highlight=True,
        get_radius=1000,          # Radius is given in meters
        get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
        pickable=True)

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=17.04,
        latitude=51.105,
        zoom=12,
        min_zoom=10,
        max_zoom=15,
        pitch=0,
        bearing=0,
    )

    # Combined all of it and render a viewport
    return pdk.Deck(layers=[layer], initial_view_state=view_state)