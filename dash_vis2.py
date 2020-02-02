
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import os
import plotly.express as px
import random

df = pd.DataFrame(columns = ['UFO_shape','country','latitude','longitude'])
path = 'updated.csv'
data = pd.read_csv(path)

number_of_colors = len(data['UFO_shape'].unique())

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
print(color)
d={}
for col_shape, color in zip(data['UFO_shape'].unique(), color):
    d[col_shape] = color

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def plot_1(country, shape):
    filtered_df = data[data.country.isin(country)]
    keys = shape & d.keys()
    print(keys)
    values = [d[key] for key in keys]
    print(values)
    filtered_df = data[data.UFO_shape.isin(shape)]
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color="UFO_shape", hover_data=["UFO_shape","length_of_encounter_seconds"],
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=3)
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="RebeccaPurple", showland=True, landcolor="yellow", showocean=True, oceancolor="LightBlue")
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        title = 'Shape of UFO Sightings around the World<br>(Hover for shapes observed)',
        autosize=False,
        hovermode='closest',
        height=800,
    )
    
    return fig

def piechart(shape):
    fig = px.pie(data, values= ufo_count.values, names=ufo_count.index, 
             title='Shapes of UFOs', color_discrete_sequence = px.colors.sequential.Jet)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
available_indicators = data['UFO_shape'].unique()
country = data['country'].unique()
ufo_count = data['UFO_shape'].value_counts()

app.layout = html.Div([
    dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': i, 'value': i} for i in country],
                value='us',
                multi=True
            ),
    dcc.Checklist(
                id='shape-button',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=list(['cylinder']),
                labelStyle={'display': 'inline-block'}
            ),
    dcc.Graph(id='alien_map'),
    dcc.Graph(id ='shape_chart')

])

@app.callback(
    [Output('alien_map', 'figure'),
    Output('shape_chart','figure')],
    [Input('country-dropdown', 'value'),
    Input('shape-button', 'value')])

def update_figure(country, shape):
    XY = list(country)
    return (plot_1(XY,shape), piechart(shape))


if __name__ == '__main__':
    app.run_server(debug=True)