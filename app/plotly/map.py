import plotly.express as px
import pandas as pd
import os

us_cities = pd.read_csv("data/estacions_bicing.csv")


fig = px.scatter_mapbox(us_cities, lat="latitude", lon="longitude", hover_name="streetName",
                        color_discrete_sequence=["red"], zoom=11)

fig.update_layout(mapbox_style="carto-positron")

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.write_html('app/templates/pages/bicing_map.html')
