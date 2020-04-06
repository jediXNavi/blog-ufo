import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from textwrap import dedent as d
import pandas as pd
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

df = pd.read_csv('updated.csv',index_col=0)

#Slider with Map
df['year'] = df['Date_time'].apply(lambda x:int(re.findall(r'...\d\s',str(x))[0].strip()))
df1 = df.groupby(['year','country'], sort=False).size().reset_index(name='Count')
year = df1['year'].to_list()

us_data = df1[df1['country']=='us']
ca_data = df1[df1['country']=='ca']
au_data = df1[df1['country']=='au']
gb_data = df1[df1['country']=='gb']

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

fig1 = go.Figure(data=[
    go.Bar(name='us', x=year,y=us_data['Count']),
    go.Bar(name='ca', x=year,y=ca_data['Count']),
    go.Bar(name='au', x=year,y=au_data['Count']),
    go.Bar(name='gb', x=year,y=gb_data['Count'])
])

# Change the bar mode
fig1.update_layout(barmode='stack')
fig1.show()

def plot_1(selected_year):
    filtered_df = df[df.year == selected_year]
    fig = go.Figure(data=go.Scattergeo(lat = filtered_df['latitude'], lon = filtered_df['longitude'], text = filtered_df['description'], showlegend = True, marker = dict(size = 10, opacity = 0.8, reversescale = True, autocolorscale = False, symbol = 'circle', color = 'mediumturquoise')))
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="RebeccaPurple", showland=True, landcolor="ghostwhite", showocean=True, oceancolor="LightBlue", showlakes=True, lakecolor="Blue", showrivers=True, rivercolor="Blue")
    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig.update_layout(title='UFO Sightings per year', autosize=True, hovermode='closest', height=600, margin={"r":0,"t":0,"l":0,"b":0})

    return fig


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='alien_map'),
    dcc.Graph(id='stack_bar'),
    dcc.Slider(
        id='year-slider',
        marks={str(year): str(year) for year in range(df['year'].min(),df['year'].max()+5,2)},
        min=df['year'].min(),
        max=df['year'].max(),
        step=1)],
    html.Div([dcc.Markdown(d("""
        **Click Data**

        Click on points in the graph.
    """)),html.Pre(id='click-data', style=styles['pre'])], className='three columns')
@app.callback(
    Output('alien_map', 'figure'),
    [Input('year-slider', 'value')])

def update_figure(X):
    return plot_1(X)

if __name__ == '__main__':
    app.run_server(debug=True)

    # 1993: {'label': 'X-Files Starts(1993)', 'style': {'color': '#f50'}}