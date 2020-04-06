# -*- coding: utf-8 -*-

import os
import pathlib
import re

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go

# import cufflinks as cf

# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server

# Load data

# APP_PATH = str(pathlib.Path(__file__).parent.resolve())
#
# df_lat_lon = pd.read_csv(
#     os.path.join(APP_PATH, os.path.join("data", "lat_lon_counties.csv"))
# )
# df_lat_lon["FIPS "] = df_lat_lon["FIPS "].apply(lambda x: str(x).zfill(5))
#
# df_full_data = pd.read_csv(
#     os.path.join(
#         APP_PATH, os.path.join("data", "age_adjusted_death_rate_no_quotes.csv")
#     )
# )
# df_full_data["County Code"] = df_full_data["County Code"].apply(
#     lambda x: str(x).zfill(5)
# )
# df_full_data["County"] = (
#     df_full_data["Unnamed: 0"] + ", " + df_full_data.County.map(str)
# )

# YEARS = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
#Data for Tab-1
# Reading data for Map with Slider
df = pd.read_csv('data.csv')
df['year'] = df['Date_time'].apply(lambda x: int(re.findall(r'...\d\s', str(x))[0].strip()))
YEARS = range(df['year'].min(), df['year'].max() + 1, 4)

df = df[df['latitude'] != '33q.200088']

# Data for Stacked Bar Chart
df1 = df.groupby(['year', 'country'], sort=False).size().reset_index(name='Count')

us_data = df1[df1['country'] == 'us']
ca_data = df1[df1['country'] == 'ca']
au_data = df1[df1['country'] == 'au']
gb_data = df1[df1['country'] == 'gb']
year = df1['year'].to_list()
# Change the bar mode

#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.#.

#Data for Tab-2
# Import data and read .csv files to create Pandas DataFram
path = 'updated.csv'
data_viz3 = pd.read_csv(path)
data_viz3.dropna()

available_indicators = data_viz3['UFO_shape'].unique()
country = data_viz3['country'].unique()
ufo_count = data_viz3['UFO_shape'].value_counts()

BINS = [
    "0-2",
    "2.1-4",
    "4.1-6",
    "6.1-8",
    "8.1-10",
    "10.1-12",
    "12.1-14",
    "14.1-16",
    "16.1-18",
    "18.1-20",
    "20.1-22",
    "22.1-24",
    "24.1-26",
    "26.1-28",
    "28.1-30",
    ">30",
]

DEFAULT_COLORSCALE = [
    "#f2fffb",
    "#bbffeb",
    "#98ffe0",
    "#79ffd6",
    "#6df0c8",
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


# Map with Slider
def MAP(selected_year):
    callback_df = df[df.year == selected_year]
    callback_df['latitude'] = callback_df['latitude'].astype(float)
    fig = px.scatter_mapbox(callback_df, lat='latitude', lon='longitude', text='description', zoom=1,
                            color_discrete_sequence=["crimson"])
    fig.update_geos(resolution=50, showcoastlines=True, coastlinecolor="darkgray", showland=True, landcolor="black",
                    showocean=True, oceancolor="darkslategrey", showlakes=True, lakecolor="darkslategrey",
                    showrivers=True, rivercolor="darkgray")
    fig.update_layout(mapbox_style="open-street-map", hovermode='closest', autosize=True,
                      margin=dict(t=0, b=0, l=0, r=0))
    fig.update_layout(paper_bgcolor="#F4F4F9", plot_bgcolor="#F4F4F9")
    return fig

# Python Plots/Functions for Callbacks and Outputs:
def plot_1(country, shape):
    filtered_df = data_viz3[data_viz3.country.isin(country)]
    filtered_df = filtered_df[filtered_df.UFO_shape.isin(shape)]
    # filtered_df['latitude'] = filtered_df['latitude'].astype(float)
    px.set_mapbox_access_token("pk.eyJ1IjoiamVkaXhuYXZpIiwiYSI6ImNrNXR4NXBheDAzbjAza241M3hmc2tocmQifQ.ifmNsmhq7kjoFWkf3jHgAg")
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color="UFO_shape", text='description', zoom=1)
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        height=800,
        margin=dict(t=0, b=0, l=0, r=0)
    )
    fig.update_layout(mapbox_style="carto-positron")

    return fig


def piechart(shape):
    fig = px.pie(data_viz3, values=ufo_count.values, names=ufo_count.index,
                 title='Shapes of UFOs', color_discrete_sequence=px.colors.sequential.Jet)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


# Static bar Chart
fig1 = go.Figure(data=[
    go.Bar(name='us', x=year, y=us_data['Count']),
    go.Bar(name='ca', x=year, y=ca_data['Count']),
    go.Bar(name='au', x=year, y=au_data['Count']),
    go.Bar(name='gb', x=year, y=gb_data['Count'])
])

fig1.update_layout(title=go.layout.Title(text="Total UFO Sightings"), margin=dict(t=52, b=0, l=0, r=0),
                   yaxis=dict(title='UFO Sightings'), barmode='stack',
                   font=dict(family="Courier New, monospace",
                             size=22,
                             color="#7f7f7f"))


app.layout = html.Div([html.Div(
    style={'background-image': 'url("assets/ufo1.jpg")'},
    id="root"),
    html.Div(
        id="header",
        children=[
            html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
            html.H4(children="UFO Sightings Across the Globe"),
            html.P(
                id="description",
                children="Ever wondered if a UFO can be shaped like a cigarette! \
                These series of visualisations using the powerful Plotly-Dash will blow your mind away! \
                ",
            ),
        ], style={'color': '#40e0d0'}
    ),
    dcc.Tabs(id="tabs", value='Tab1', children=[
        dcc.Tab(label='Tab 1',
                id='tab1',
                value='Tab1',
                children =[html.Div(
                id="app-container",
                children=[
                    html.Div(
                        id="left-column",
                        children=[
                            html.Div(
                                id="slider-container",
                                children=[
                                    html.P(
                                        id="slider-text",
                                        children="Drag the slider to change the year:",
                                    ),
                                    dcc.Slider(
                                        id="years-slider",
                                        min=min(YEARS),
                                        max=max(YEARS),
                                        value=min(YEARS),
                                        marks={
                                            str(year): {
                                                "label": str(year),
                                                "style": {"color": "#7fafdf"},
                                            }
                                            for year in YEARS
                                        },
                                    ),
                                ],
                            ),
                            html.Div(
                                id="heatmap-container",
                                children=[
                                    html.P(
                                        "Number of UFO sightings \
                                        in year {0}".format(
                                            min(YEARS)
                                        ),
                                        id="heatmap-title",
                                    ),
                                    html.Div(id='text-content'),
                                    # dcc.Graph(id='UFO_map'),
                                    dcc.Graph(
                                        id="UFO_map",
                                        figure=dict(
                                            # data=[
                                            #     dict(
                                            #         lat=df_lat_lon["Latitude "],
                                            #         lon=df_lat_lon["Longitude"],
                                            #         text=df_lat_lon["Hover"],
                                            #         type="scattermapbox",
                                            #     )
                                            # ],
                                            layout=dict(
                                                mapbox=dict(
                                                    layers=[],
                                                    accesstoken=mapbox_access_token,
                                                    style=mapbox_style,
                                                    center=dict(
                                                        lat=38.72490, lon=-95.61446
                                                    ),
                                                    pitch=0,
                                                    zoom=3.5,
                                                ),
                                                autosize=True,
                                            ),
                                        ),
                                    ),
                                    dcc.Graph(id='bar_chart', figure=fig1)
                                ], style={'color': '#40e0d0'},
                            ),
                        ],
                ),
            ],
        )]),
        dcc.Tab(label='Tab 2',
                id='tab2',
                value= 'Tab2',
                children=[html.Div([


    dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': i, 'value': i} for i in country],
                multi=True,
                value = list(['us'])
            ),
    dcc.Checklist(
                id='shape-button',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=list(['cylinder']),
                labelStyle={'display': 'inline-block'}
            ),
    html.Div(id='text-content1'),
    dcc.Graph(id='UFO_map1'),
    html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
    dcc.Graph(id ='shape_chart')])])
        ])
])
# App layout
@app.callback(Output("heatmap-title", "children"), [Input("years-slider", "value")])
def update_map_title(year):
    return "Number of UFO Sightings in the year {0}".format(
        year
    )
@app.callback(Output('UFO_map', 'figure'), [Input('years-slider', 'value')])
def update_figure(selected_year):
    return MAP(selected_year)
@app.callback(Output('text-content', 'children'), [Input('UFO_map', 'hoverData')])
def update_text_map1(hoverData):
    if hoverData is not None:
        text = hoverData['points'][0]['text']
        return html.H6('UFO Description: ' + text, style={'color': 'violet', 'fontsize': 10})
@app.callback(
    [Output('UFO_map1', 'figure'),
    Output('shape_chart','figure')],
    [Input('country-dropdown', 'value'),
    Input('shape-button', 'value')])
def update_figure(country, shape):
    XY = list(country)
    return (plot_1(XY,shape), piechart(shape))
@app.callback(Output('text-content1','children'),[Input('UFO_map1','hoverData')])
def update_text_map2(hoverData1):
    if hoverData1 is not None:
        text = hoverData1['points'][0]['text']
        return html.H4(f'UFO Description: {text},',style={'color': 'red', 'fontSize': 18})
# @app.callback(
#     Output("county-choropleth", "figure"),
#     [Input("years-slider", "value")],
#     [State("county-choropleth", "figure")],
# )
# def display_map(year, figure):
#     cm = dict(zip(BINS, DEFAULT_COLORSCALE))

#     data = [
#         dict(
#             lat=df_lat_lon["Latitude "],
#             lon=df_lat_lon["Longitude"],
#             text=df_lat_lon["Hover"],
#             type="scattermapbox",
#             hoverinfo="text",
#             marker=dict(size=5, color="white", opacity=0),
#         )
#     ]

#     annotations = [
#         dict(
#             showarrow=False,
#             align="right",
#             text="<b>Age-adjusted death rate<br>per county per year</b>",
#             font=dict(color="#2cfec1"),
#             bgcolor="#1f2630",
#             x=0.95,
#             y=0.95,
#         )
#     ]

#     for i, bin in enumerate(reversed(BINS)):
#         color = cm[bin]
#         annotations.append(
#             dict(
#                 arrowcolor=color,
#                 text=bin,
#                 x=0.95,
#                 y=0.85 - (i / 20),
#                 ax=-60,
#                 ay=0,
#                 arrowwidth=5,
#                 arrowhead=0,
#                 bgcolor="#1f2630",
#                 font=dict(color="#2cfec1"),
#             )
#         )

#     if "layout" in figure:
#         lat = figure["layout"]["mapbox"]["center"]["lat"]
#         lon = figure["layout"]["mapbox"]["center"]["lon"]
#         zoom = figure["layout"]["mapbox"]["zoom"]
#     else:
#         lat = (38.72490,)
#         lon = (-95.61446,)
#         zoom = 3.5

#     layout = dict(
#         mapbox=dict(
#             layers=[],
#             accesstoken=mapbox_access_token,
#             style=mapbox_style,
#             center=dict(lat=lat, lon=lon),
#             zoom=zoom,
#         ),
#         hovermode="closest",
#         margin=dict(r=0, l=0, t=0, b=0),
#         annotations=annotations,
#         dragmode="lasso",
#     )

#     base_url = "https://raw.githubusercontent.com/jackparmer/mapbox-counties/master/"
#     for bin in BINS:
#         geo_layer = dict(
#             sourcetype="geojson",
#             source=base_url + str(year) + "/" + bin + ".geojson",
#             type="fill",
#             color=cm[bin],
#             opacity=DEFAULT_OPACITY,
#             # CHANGE THIS
#             fill=dict(outlinecolor="#afafaf"),
#         )
#         layout["mapbox"]["layers"].append(geo_layer)

#     fig = dict(data=data, layout=layout)
#     return fig

# @app.callback(
#     Output("selected-data", "figure"),
#     [
#         Input("county-choropleth", "selectedData"),
#         Input("chart-dropdown", "value"),
#         Input("years-slider", "value"),
#     ],
# )
# def display_selected_data(selectedData, chart_dropdown, year):
#     if selectedData is None:
#         return dict(
#             data=[dict(x=0, y=0)],
#             layout=dict(
#                 title="Click-drag on the map to select counties",
#                 paper_bgcolor="#1f2630",
#                 plot_bgcolor="#1f2630",
#                 font=dict(color="#2cfec1"),
#                 margin=dict(t=75, r=50, b=100, l=75),
#             ),
#         )
#     pts = selectedData["points"]
#     fips = [str(pt["text"].split("<br>")[-1]) for pt in pts]
#     for i in range(len(fips)):
#         if len(fips[i]) == 4:
#             fips[i] = "0" + fips[i]
#     dff = df_full_data[df_full_data["County Code"].isin(fips)]
#     dff = dff.sort_values("Year")

#     regex_pat = re.compile(r"Unreliable", flags=re.IGNORECASE)
#     dff["Age Adjusted Rate"] = dff["Age Adjusted Rate"].replace(regex_pat, 0)

#     if chart_dropdown != "death_rate_all_time":
#         title = "Absolute deaths per county, <b>1999-2016</b>"
#         AGGREGATE_BY = "Deaths"
#         if "show_absolute_deaths_single_year" == chart_dropdown:
#             dff = dff[dff.Year == year]
#             title = "Absolute deaths per county, <b>{0}</b>".format(year)
#         elif "show_death_rate_single_year" == chart_dropdown:
#             dff = dff[dff.Year == year]
#             title = "Age-adjusted death rate per county, <b>{0}</b>".format(year)
#             AGGREGATE_BY = "Age Adjusted Rate"

#         dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors="coerce")
#         deaths_or_rate_by_fips = dff.groupby("County")[AGGREGATE_BY].sum()
#         deaths_or_rate_by_fips = deaths_or_rate_by_fips.sort_values()
#         # Only look at non-zero rows:
#         deaths_or_rate_by_fips = deaths_or_rate_by_fips[deaths_or_rate_by_fips > 0]
#         fig = deaths_or_rate_by_fips.iplot(
#             kind="bar", y=AGGREGATE_BY, title=title, asFigure=True
#         )

#         fig_layout = fig["layout"]
#         fig_data = fig["data"]

#         fig_data[0]["text"] = deaths_or_rate_by_fips.values.tolist()
#         fig_data[0]["marker"]["color"] = "#2cfec1"
#         fig_data[0]["marker"]["opacity"] = 1
#         fig_data[0]["marker"]["line"]["width"] = 0
#         fig_data[0]["textposition"] = "outside"
#         fig_layout["paper_bgcolor"] = "#1f2630"
#         fig_layout["plot_bgcolor"] = "#1f2630"
#         fig_layout["font"]["color"] = "#2cfec1"
#         fig_layout["title"]["font"]["color"] = "#2cfec1"
#         fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
#         fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
#         fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
#         fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
#         fig_layout["margin"]["t"] = 75
#         fig_layout["margin"]["r"] = 50
#         fig_layout["margin"]["b"] = 100
#         fig_layout["margin"]["l"] = 50

#         return fig

#     fig = dff.iplot(
#         kind="area",
#         x="Year",
#         y="Age Adjusted Rate",
#         text="County",
#         categories="County",
#         colors=[
#             "#1b9e77",
#             "#d95f02",
#             "#7570b3",
#             "#e7298a",
#             "#66a61e",
#             "#e6ab02",
#             "#a6761d",
#             "#666666",
#             "#1b9e77",
#         ],
#         vline=[year],
#         asFigure=True,
#     )

#     for i, trace in enumerate(fig["data"]):
#         trace["mode"] = "lines+markers"
#         trace["marker"]["size"] = 4
#         trace["marker"]["line"]["width"] = 1
#         trace["type"] = "scatter"
#         for prop in trace:
#             fig["data"][i][prop] = trace[prop]

#     # Only show first 500 lines
#     fig["data"] = fig["data"][0:500]

#     fig_layout = fig["layout"]

#     # See plot.ly/python/reference
#     fig_layout["yaxis"]["title"] = "Age-adjusted death rate per county per year"
#     fig_layout["xaxis"]["title"] = ""
#     fig_layout["yaxis"]["fixedrange"] = True
#     fig_layout["xaxis"]["fixedrange"] = False
#     fig_layout["hovermode"] = "closest"
#     fig_layout["title"] = "<b>{0}</b> counties selected".format(len(fips))
#     fig_layout["legend"] = dict(orientation="v")
#     fig_layout["autosize"] = True
#     fig_layout["paper_bgcolor"] = "#1f2630"
#     fig_layout["plot_bgcolor"] = "#1f2630"
#     fig_layout["font"]["color"] = "#2cfec1"
#     fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
#     fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
#     fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
#     fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"

#     if len(fips) > 500:
#         fig["layout"][
#             "title"
#         ] = "Age-adjusted death rate per county per year <br>(only 1st 500 shown)"

#     return fig

# @app.callback(
#     Output('text-content','children'),
#     [Input('UFO_map','hoverData')])

# def update_text(hoverData):
#     if hoverData is not None:
#         text = hoverData['points'][0]['text']
#         return html.H3(f'{text}')

if __name__ == "__main__":
    app.run_server(debug=True)
