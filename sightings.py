import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('/home/arjun/Documents/SFU_Course_Work/Spring2020/cmpt733/blog/blog_git/blog-733/updated.csv')

fig = go.Figure()

# Trial comment for git

fig.add_trace(go.Scattermapbox(
        lat=df.latitude,
        lon=df.longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=3,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=df.description,
        hoverinfo='text'
    ))

fig.update_layout(
    title='UFO Sightings Location and Shape',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    geo = dict(
        lataxis = dict(showgrid = True),
        lonaxis = dict(showgrid = True)),
    mapbox=go.layout.Mapbox(
        accesstoken="pk.eyJ1Ijoia2Rlc2FpMTciLCJhIjoiY2s1a2ZzYnlsMGRxcDNrcWxuY245N3M4aiJ9.c1k9nyK3is0jBi9USem_GQ",
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=-3,
        style='light'
    ),
)

fig.show()

if __name__ == "__main__":
    app.run_server(debug=True)
