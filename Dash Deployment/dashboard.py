#importing libraries
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd


app = Dash(__name__)

#-- Import and clean data (importing csv into pandas)
df = pd.read_csv("C:\Data Science\Jupyter_Workspace\Twitter_Sentiment\Data\JSONLs\\final_df.csv")
#print(df[:5]) #printing out a sample to verify if it's correct or not

# Importing the GeoJSON File
import geojson
with open("C:\Data Science\Jupyter_Workspace\Twitter_Sentiment\Dash Deployment\states_india.geojson") as f:
    india_states = geojson.load(f)

#connecting state column to geojson with id mapping    
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["st_nm"]


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Sentiment Timeline for Covid-19 in India 2021-22", 
            style={'color': "#004c40", 'font-family': 'Helvetica', 'text-align': 'center'}),
    html.H4("Sentiment analysis is a way to quantify the feeling or tone of written text. In a survey context, this is a useful technique for gauging the overall attitude towards a brand, product, or feature. In sentiment analysis, each case receives a numeric sentiment score (on a negative to positive scale)", 
            style={'color': "#00796b", 'font-family': 'Helvetica', 'text-align': 'left'}),

    dcc.Dropdown(id="selected_date",
                 options=[
                     {"label": "March 20, 2020", "value": 20200320},
                     {"label": "March 25, 2020", "value": 20200325},
                     {"label": "March 27, 2020", "value": 20200327},
                     {"label": "March 30, 2020", "value": 20200330}],
                 multi=False,
                 value=20200320,
                 style={'width': "40%"}
                 ),

    html.Br(),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='sentiment_map', figure={})
    #dcc.Graph(id='my-graph',style={'width': '90vh', 'height': '90vh'})  #uses half the screen

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='sentiment_map', component_property='figure')],
    [Input(component_id='selected_date', component_property='value')]
)
def update_graph(date_selected):
    print(date_selected)
    print(type(date_selected))

    dff = df.copy()
    dff = dff[dff["date"] == date_selected]
    #message = dff["date_info"].iloc[0]
    
    #container = message
    container = "The date chosen by user was: {}".format(date_selected)

    # Plotly Express
    fig = px.choropleth_mapbox(
        data_frame = dff, 
        locations = 'state', 
        geojson = india_states,
        range_color=(-1, 1),
        color = 'vader_score', 
        mapbox_style = "carto-positron",
        color_continuous_scale = px.colors.diverging.RdBu, 
        color_continuous_midpoint = 0,
        center = {'lat': 23, 'lon': 82}, 
        zoom = 3.00, 
        labels = {'vader_score': 'Sentiment Score', 'state': 'State'},
        )
    
    fig.update_layout(margin=dict(
        l=20, 
        r=20, 
        t=20, 
        b=20, 
        pad=5),
        paper_bgcolor="#b2dfdb", 
        autosize=False,
        width=600,
        height=430)
    
    #fig.update_coloraxes(colorbar_xanchor="right")

    return container, fig


# --------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)