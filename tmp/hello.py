from flask import Flask, render_template
from random import randint
from flask_bootstrap import Bootstrap

import altair as alt

# load a sample dataset as a pandas DataFrame
from vega_datasets import data



app=Flask(__name__)
bootstrap=Bootstrap(app)

@app.route("/rand")
def hello():
    x=randint(1,10)
    cars = data.cars()
    alt.renderers.enable('json')

    # make the chart
    picture=alt.Chart(cars).mark_point().encode(
        x='Horsepower',
        y='Miles_per_Gallon',
        color='Origin',
    )#.interactive()
    #print(picture.seve('json'))
    return render_template("index.html", value=2*x, picture=picture.to_json())




