import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd
import re

# Import data and read .csv files to create Pandas DataFrame, Grouping. 
df = pd.read_csv('data.csv',index_col=0)
df['year'] = df['Date_time'].apply(lambda x:int(re.findall(r'...\d\s',str(x))[0].strip()))
df_year_list = df.groupby(['year','country'], sort=False).size().reset_index(name='Count')


# Import Styling External Sheets for HTML/CSS Web Layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Python Plots/Functions for Callbacks and Outputs: 
def MAP(selected_year):
    callback_df = df[df.year == selected_year]
    callback_df['latitude'] = callback_df['latitude'].astype(float)
    fig = px.scatter_mapbox(callback_df,lat = 'latitude', lon = 'longitude',text='description',zoom=1.45,color_discrete_sequence=['crimson'])
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="darkgray", showland=True, landcolor="black", showocean=True, oceancolor="darkslategrey", showlakes=True, lakecolor="darkslategrey", showrivers=True, rivercolor="darkgray")
    fig.update_layout(mapbox_style="open-street-map",height=400,hovermode='closest',autosize=False,
                      margin=dict(t=2, b=2, l=2, r=2))
    return fig

# Create Dash app. 
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

# Define Dash App Layout: app.layout using HTML tags.
app.layout = html.Div([
    # Text Decription of UFO
    html.Div(id='text-content'),
    # Figure1: MAP
    dcc.Graph(id='UFO_map'),
        dcc.Slider(
        id='year-slider',
        marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1,4)},
        min=df['year'].min(),
        max=df['year'].max(),
        value=1993,
        step=1),
])
    # Figure2: Slider


# Define to update Output: Graph - Map Scatter based on Slider Input
@app.callback(
    Output('UFO_map', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(selected_year):
    return MAP(selected_year)

# Define second callback to update text/header using "Description" 
#                                   while hovering over the points
@app.callback(
    Output('text-content','children'),
    [Input('UFO_map','hoverData')])

def update_text(hoverData):
    if hoverData is not None:
        text = hoverData['points'][0]['text']
        return html.H2(f'UFO Description :{text}',style={'color': 'red', 'fontSize': 18})

if __name__ == '__main__':
    app.run_server(debug=True)

