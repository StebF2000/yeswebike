
import plotly.express as px
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import psycopg2 as psy

conn = psy.connect(
    dbname="postgres",
    user="admin",
    host="172.28.1.4",
    password="admin"
)

df = pd.read_query('select * from estat', conn)
fig = px.scatter_mapbox(df.iloc[:int(1e3)], lat="lat", lon="lon",
                        animation_frame='last_updated',
                        color="status", size=" num_bikes_available_types.mechanical",
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        size_max=10, zoom=12,
                        title='Visualizing spread of COVID from 22/1/2020 to17/6/2020')
fig.update_layout(mapbox_style="carto-positron")
fig.update_layout(template='plotly_white')
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
data_canada = px.data.gapminder().query("country == 'Canada'")
fig2 = px.bar(data_canada, x='year', y='pop')

fig.add_trace(fig2)

fig.show()
