import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
from dataprep.eda import plot_missing
import os

df = pd.DataFrame(columns = ['station', 'date', 'latitude', 'longitude', 'elevation', 'tmax'])
path = '/home/arjun/Documents/SFU_Course_Work/Spring2020/cmpt733/A3/part2/tmax-2'
for filename in os.listdir(path):
    data = pd.read_csv(path+'/'+filename, compression='gzip', header = None, names = ['station', 'date', 'latitude', 'longitude', 'elevation', 'tmax'])
    df = df.append(data, ignore_index=True)

df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
group_df = df.groupby(['year','month','station','latitude', 'longitude', 'elevation'], as_index=False, sort = True)['tmax'].max()#sum function
group_df = group_df[group_df['year']>1980.5]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=group_df['year'].min(),
        max=group_df['year'].max(),
        value=group_df['year'].min(),
        marks={str(year): str(year) for year in group_df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(selected_year):
    filtered_df = group_df[group_df.year == selected_year]
    fig = go.Figure(data=go.Scattergeo(lat = filtered_df['latitude'], lon = filtered_df['longitude'], text = filtered_df['tmax'], showlegend = True, marker = dict(size = 10, opacity = 0.8, reversescale = True, autocolorscale = False, symbol = 'square', colorscale = 'icefire_r', cmin = -35, color = group_df['tmax'], cmax = 50, colorbar_title="Max Temp")))
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="RebeccaPurple", showland=True, landcolor="ghostwhite", showocean=True, oceancolor="LightBlue", showlakes=True, lakecolor="Blue", showrivers=True, rivercolor="Blue")
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig.update_layout(title='Global Maximum Temperature ', autosize=True, hovermode='closest', height=600, margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    #return(fig.show())

if __name__ == '__main__':
	app.run_server(debug=True)