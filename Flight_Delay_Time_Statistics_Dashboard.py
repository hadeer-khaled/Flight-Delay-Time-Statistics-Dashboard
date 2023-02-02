import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html , dcc, Input, Output

# external_stylesheets = ['stylesheet.css']
# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Create a dash application
app = dash.Dash(__name__ )
app.title = "Dashborad Practise 2"

app.layout = html.Div(className="container",
                    children=[
                            html.H1('Flight Delay Time Statistics',className="title",),   
                            html.Div(className="title-line"),                             
                            html.Div(className="input-div",children=
                                    ["Input Year: ",
                                    dcc.Input(id='input-year', value='2010',  type='number',placeholder="Enter a year from 2010 and 2020")
                                    ]
                                    ),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                        html.Div(dcc.Graph(id="carrier-plot")),
                                        html.Div(dcc.Graph(id="weather-plot"))
                                    ],style={'display': 'flex'}),
                            html.Div([
                                        html.Div(dcc.Graph(id="nas-plot")),
                                        html.Div(dcc.Graph(id="security-plot"))
                                    ],style={'display': 'flex'}),                                
                            html.Div(className = "late-plot",children=[html.Div(dcc.Graph(id="late-plot"))]),    
                            ]
                    )

""" Compute_info function description

This function takes in airline data and selected year as an input and performs computation for creating charts and plots.

Arguments:
    airline_data: Input airline data.
    entered_year: Input year for which computation needs to be performed.
    
Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.

"""

def compute_info(airline_data, entered_year):
    # Select data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    # Compute delay averages
    avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

@app.callback( [
               Output(component_id='carrier-plot', component_property='figure'),
               Output(component_id='weather-plot', component_property='figure'),
               Output(component_id='nas-plot', component_property='figure'),
               Output(component_id='security-plot', component_property='figure'),
               Output(component_id='late-plot', component_property='figure')
               ],
               Input(component_id = "input-year" ,component_property='value')
            )
# Computation to callback function and return graph
def get_graph(entered_year):
    
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
            
    # Line plot for carrier delay
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrier delay time (minutes) by airline')
    carrier_fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)", font =dict(color="white"))

    # Line plot for weather delay
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average WeatherDelay time (minutes) by airline')
    weather_fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",font =dict(color="white"))

    # Line plot for nas delay
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NASDelay time (minutes) by airline')
    nas_fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",font =dict(color="white"))
    # Line plot for security delay
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average SecurityDelay time (minutes) by airline')
    sec_fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",font =dict(color="white"))
    # Line plot for late aircraft delay
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average LateAircraftDelay time (minutes) by airline')
    late_fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor = "rgba(0,0,0,0)",font =dict(color="white"))

    return[carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

# Run the app
if __name__ == '__main__':
    app.run_server()