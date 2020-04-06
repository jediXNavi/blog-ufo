import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re
import plotly.graph_objects as go


df = pd.read_csv('data.csv',index_col=0)
df.dropna()
#Slider with Map
df['year'] = df['Date_time'].apply(lambda x:int(re.findall(r'...\d\s',str(x))[0].strip()))
df1 = df.groupby(['year','country'], sort=False).size().reset_index(name='Count')
year = df1['year'].to_list()

us_data = df1[df1['country']=='us']
ca_data = df1[df1['country']=='ca']
au_data = df1[df1['country']=='au']
gb_data = df1[df1['country']=='gb']

fig1 = go.Figure(data=[
    go.Bar(name='us', x=year,y=us_data['Count']),
    go.Bar(name='ca', x=year,y=ca_data['Count']),
    go.Bar(name='au', x=year,y=au_data['Count']),
    go.Bar(name='gb', x=year,y=gb_data['Count'])
])

# Change the bar mode
fig1.update_layout(title=go.layout.Title(text="Total UFO Sightings"),    yaxis=dict(title='UFO Sightings'),barmode='stack',font=dict(
        family="Courier New, monospace",
        size=22,
        color="#7f7f7f"
    ))
fig1.show()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div(id='text-content'),
    dcc.Graph(id='bar_chart')])

if __name__ == '__main__':
    app.run_server(debug=True)