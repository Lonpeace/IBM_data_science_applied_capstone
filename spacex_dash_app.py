# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options = [
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                            value = 'ALL',
                                            placeholder = 'Select a launch site here',
                                            searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks = {
                                                    0: '0',
                                                    100: '100'
                                                },
                                                value = [min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def pieChart(site):
    if site == 'ALL':
        fig = px.pie(
            spacex_df,
            values = 'class',
            names = 'Launch Site',
            title = 'Total success launches by site'
        )
    else:
        filteredDf = spacex_df[spacex_df['Launch Site'] == site]
        filteredDf = filteredDf.groupby('class').count().reset_index()
        fig = px.pie(
            filteredDf,
            values = 'Unnamed: 0',
            names = 'class',
            title = f'Total launches for site {site}'
        )
    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value"))
def scatterChart(site, payloadRange):
    if site == 'ALL':
        filteredDf = spacex_df[(spacex_df['Payload Mass (kg)'] >= int(payloadRange[0])) &
                                (spacex_df['Payload Mass (kg)'] <= int(payloadRange[1]))]

        fig = px.scatter(filteredDf, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = f'All sites - payload mass between {int(payloadRange[0])}kg and {payloadRange[1]}kg')
    else:
        filteredDf = spacex_df[
            (spacex_df['Launch Site'] == site) & 
            (spacex_df['Payload Mass (kg)'] >= int(payloadRange[0])) &
            (spacex_df['Payload Mass (kg)'] <= int(payloadRange[1]))
        ]
        fig = px.scatter(filteredDf, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title = f'{site} - payload mass between {int(payloadRange[0])}kg and {payloadRange[1]}kg')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
