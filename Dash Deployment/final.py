#importing libraries
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


app = Dash(__name__)
app = dash.Dash(external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"
])


#-- Import and clean data (importing csv into pandas)
df = pd.read_csv("C:\Data Science\GitHub Projects\Twitter-Sentiment-Analysis\\final_df.csv")
#print(df[:5]) #printing out a sample to verify if it's correct or not

# Importing the GeoJSON File
import geojson
with open("C:\Data Science\GitHub Projects\Twitter-Sentiment-Analysis\Dash Deployment\states_india.geojson") as f:
    india_states = geojson.load(f)

#connecting state column to geojson with id mapping    
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["st_nm"]


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Sentiment Timeline for Covid-19 in India 2021-22", 
            style={'color': "#004d40", 'font-family': 'Helvetica', 'text-align': 'center'}),
    html.H4("Sentiment Analysis is a way to quantify the tone of a written text. Using this, we can see if people are feeling negative, neutral or positive during a certain event; in this case, through Twitter. Here you can get a numeric sentiment score on a negative (-1) to positive scale (+1) for each state in India and compare the Mappings across significant Covid-related events in 2021-22.", 
            style={'color': "#263238", 'font-family': 'Helvetica', 'text-align': 'left'}),
    
    dbc.Row([
        dbc.Col(html.Div([
            dcc.Markdown('''
                         Please select the **first date** below:
                        '''),
            dcc.Dropdown(
                id="selected_date_1",
                options=[
                     {"label": "March 20, 2020", "value": 20200320},
                     {"label": "March 25, 2020", "value": 20200325},
                     {"label": "March 27, 2020", "value": 20200327},
                     {"label": "April 05, 2020", "value": 20200405},
                     {"label": "May 01, 2020", "value": 20200501},
                     {"label": "May 17, 2020", "value": 20200517},],
                multi=False,
                value=20200320,
                style={'width': "100%"}
                ),
            html.Br(),
            html.Div(id='output_container_1', children=[]),
            html.Br(),
            dcc.Graph(id='sentiment_map_1', figure={}),
            #dcc.Graph(id='my-graph',style={'width': '90vh', 'height': '90vh'})  #uses half the screen
            ]), width = {'size':6}
        ),
        
        dbc.Col(html.Div([
            dcc.Markdown('''
                         Please select the **second date** below:
                        '''),
            dcc.Dropdown(
                id="selected_date_2",
                options=[
                     {"label": "March 20, 2020", "value": 20200320},
                     {"label": "March 25, 2020", "value": 20200325},
                     {"label": "March 27, 2020", "value": 20200327},
                     {"label": "April 05, 2020", "value": 20200405},
                     {"label": "May 01, 2020", "value": 20200501},
                     {"label": "May 17, 2020", "value": 20200517},],
                multi=False,
                value=20200517,
                style={'width': "100%"}
                ),
            html.Br(),
            html.Div(id='output_container_2', children=[]),
            html.Br(),
            dcc.Graph(id='sentiment_map_2', figure={}),
            #dcc.Graph(id='my-graph',style={'width': '90vh', 'height': '90vh'})  #uses half the screen
            ]), width = {'size':6}
        ),
    ]),
])



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container_1', component_property='children'),
     Output(component_id='sentiment_map_1', component_property='figure'),
     Output(component_id='output_container_2', component_property='children'),
     Output(component_id='sentiment_map_2', component_property='figure')],
    [Input(component_id='selected_date_1', component_property='value'),
     Input(component_id='selected_date_2', component_property='value')]
)
def update_graph(date_selected_1, date_selected_2):
    #for Graph 1
    dff1 = df.copy()
    dff1 = dff1[dff1["date"] == date_selected_1]
    
    message = dff1["date_info"].iloc[0]
    container_1 = message
    
    # Plotly Express
    fig1 = px.choropleth_mapbox(
        data_frame = dff1, 
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
        opacity = 0.8,
        )
    #fig1.update_layout(hovermode='x unified', legend=dict(title= None), hoverlabel=dict(bgcolor='rgba(255,255,255,0.75)',

    
    fig1.update_layout(margin=dict(
        l=20, 
        r=20, 
        t=20, 
        b=20, 
        pad=5),
        paper_bgcolor="#e8f5e9", 
        autosize=False,
        width=600,
        height=430,
        hovermode='x unified', legend=dict(title= None), hoverlabel=dict(bgcolor='#e8f5e9'),
        )
    
    
    #for Graph 2
    dff2 = df.copy()
    dff2 = dff2[dff2["date"] == date_selected_2]
    
    message2 = dff2["date_info"].iloc[0]
    container_2 = message2
    

    # Plotly Express
    fig2 = px.choropleth_mapbox(
        data_frame = dff2, 
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
        opacity = 0.8,
        )
    
    fig2.update_layout(margin=dict(
        l=20, 
        r=20, 
        t=20, 
        b=20, 
        pad=5),
        paper_bgcolor="#e8eaf6", 
        autosize=False,
        width=600,
        height=430,
        hovermode='x unified', legend=dict(title= None), hoverlabel=dict(bgcolor='#e8eaf6'),
        )
    
    
    return container_1, fig1, container_2, fig2


# --------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)