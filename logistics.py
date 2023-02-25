import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt

# loading the dataset
bi = pd.read_csv("datasets/cleandata.csv")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        # filter column
        dbc.Col([
            html.H1('Filters'),
            # Time to Start Slider
            html.Div([
                html.Label(
                'Time to Start (days)'
                ),
                dcc.RangeSlider(
                    id='home_tts',
                    min=0,
                    max=100,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ]),
            # Cost to Start Slider
            html.Div([
                html.Label(
                    "Cost to Start ('%' of income per capita)"
                ),
                dcc.RangeSlider(
                    id='home_cts',
                    min=0,
                    max=100,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ])
        ], 
        md=3,
        style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}
        ),
        # tabs column
        dbc.Col([
            # tabs
            dbc.Tabs([
                # Home Tab
                dbc.Tab([
                    # filters portion
                    dbc.Row([
                        dbc.Col(
                            # dropdown for country
                            dcc.Dropdown(
                                id='countries',
                                placeholder='Select countries...',
                                value='Canada',
                                options=[{
                                    'label': country, 'value': country
                                } for country in bi['Country Name'].unique()],
                                multi=True
                            )
                        ),
                        dbc.Col(
                            # dropdown for years
                            dcc.Dropdown(
                                id='years',
                                placeholder='Select years...',
                                #years = [2014, 2015, 2016, 2017, 2018, 2019]
                                value=2014,
                                options=[{
                                    'label': year, 'value': year
                                } for year in bi.columns if year.isdigit()],
                                multi=True
                            )
                        )
                    ])
                ], label='Home'),
                # Resources Tab
                dbc.Tab([
                    
                ], label='Resources'),
                # Logistics Tab
                dbc.Tab([
                    
                ], label='Logistics')
            ])
        ])
    ])
])

# Set up callbacks/backend
# @app.callback(

# )

if __name__ == '__main__':
    app.run_server(debug=True)