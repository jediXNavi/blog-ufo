import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import re
import plotly.express as px

df = pd.read_csv('data.csv',index_col=0)

df['year'] = df['Date_time'].apply(lambda x:int(re.findall(r'...\d\s',str(x))[0].strip()))
df1 = df.groupby(['year','country'], sort=False).size().reset_index(name='Count')
print(len(df1))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def plot_1(selected_year):
    filtered_df = df[df.year == selected_year]
    filtered_df['latitude'] = filtered_df['latitude'].astype(float)
    fig = px.scatter_mapbox(filtered_df,lat = 'latitude', lon = 'longitude',text='description',zoom=1.45)
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="darkgray", showland=True, landcolor="black", showocean=True, oceancolor="darkslategrey", showlakes=True, lakecolor="darkslategrey", showrivers=True, rivercolor="darkgray")
    fig.update_layout(height=800,hovermode='closest',autosize=False)
    fig.update_layout(mapbox_style="mapbox://styles/mapbox/light-v10", mapbox_accesstoken='pk.eyJ1IjoiamVkaXhuYXZpIiwiYSI6ImNrNXR4NXBheDAzbjAza241M3hmc2tocmQifQ.ifmNsmhq7kjoFWkf3jHgAg')

    return fig

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(id='text-content'),
    dcc.Graph(id='alien_map'),
    dcc.Slider(
        id='year-slider',
        marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1,2)},
        min=df['year'].min(),
        max=df['year'].max(),
        value=1993,
        step=1)])
@app.callback(
    Output('alien_map', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(X):
    return plot_1(X)
@app.callback(
    Output('text-content','children'),
    [Input('alien_map','hoverData')])
def update_text(hoverData):
    if hoverData is not None:
        text = hoverData['points'][0]['text']
        return html.H3(f'{text}')

if __name__ == '__main__':
    app.run_server(debug=True)

