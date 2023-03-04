import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt


# loading the dataset
bi = pd.read_csv("datasets/melted_data.csv")
latlon = pd.read_csv("datasets/world_country_and_usa_states_latitude_and_longitude_values.csv")

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    # filters row
    dbc.Row([
        # side filter column
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
                    "Cost to Start (%' of income per capita)"
                ),
                dcc.RangeSlider(
                    id='home_cts',
                    min=0,
                    max=500,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ]),
            html.Br(),
            # Average Interest Rate Slider
            html.Div([
                html.Label(
                'Average Interest Rate (%)'
                ),
                dcc.RangeSlider(
                    id='resources_air',
                    min=0,
                    max=30,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ]),
            html.Br(),
            # Time to Export Slider
            html.Div([
                html.Label(
                'Time to Export (hours)'
                ),
                dcc.RangeSlider(
                    id='logistics_tte',
                    min=0,
                    max=200,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ]),
            # Time to Import Slider
            html.Div([
                html.Label(
                'Time to Import (hours)'
                ),
                dcc.RangeSlider(
                    id='logistics_tti',
                    min=0,
                    max=200,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ]),
            # Custom Clearance Slider
            html.Div([
                html.Label(
                'Custom Clearance'
                ),
                dcc.Input(
                    id='logistics_cc',
                    placeholder="Value",
                    type='number',
                    inputMode='numeric',
                    min=0,
                    max=30,
                    value=5
                )
            ]),
        ], 
        md=3,
        style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}
        ),
        # end of side filter column
        # tabs column
        dbc.Col([
            html.H1("New Venture(s) Compass", style={"textAlign": "center"}),
            html.Hr(),
            # top filters row
            dbc.Row([
                # top filters portion
                dbc.Col(
                    # dropdown for country
                    dcc.Dropdown(
                        id='countries',
                        placeholder='Select countries...',
                        value=['Canada'],
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
                        value=['2014'],
                        options=[{
                            'label': year, 'value': year
                        } for year in bi['year'].unique()],
                        multi=True
                    )
                )
                # end of top filters portion
            ]),
            # end of top filters row
            html.Br(),
            # tabs row
            dbc.Row([
                # tabs
                dbc.Tabs(id='tabs', children=[
                    # Home Tab
                    dbc.Tab(label='Home', children=[
                       dbc.Row([
                            dbc.Col([
                                html.H5("map)"),
                                html.Iframe(
                                    id='hm_map',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                            ]),
                            dbc.Col([
                                html.H5("firstchart)"),
                                html.Iframe(
                                    id='hm_line',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                            ])
                        ])                        
                    ])
                    # end of home tab
                ])
                # end of tabs
            ])
            # end of tabs row
        ])
        # end of tabs column
    ])
    # end of filters row
])

# callback for home line chart
@app.callback(
    Output(component_id="hm_map", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value")
)

def plot_map(countries, years, home_cts):
    #latlong data
    # Data source - https://www.kaggle.com/datasets/paultimothymooney/latitude-and-longitude-for-every-country-and-state
    #which is based on https://developers.google.com/public-data/docs/canonical/countries_csv

    arr=home_cts
    #data input for selected countries

    countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & 
                                                (bi['year'].isin(years)) & 
                                                (bi['Series Name']=="Cost of business start-up procedures (% of GNI per capita)") &
                                                (bi['value']<arr[1])]
    mergedf=pd.merge(countries_years_series_filtered, latlon, how='left',left_on='Country Name',right_on='country')

    states = alt.topo_feature(data.us_10m.url, feature='states')
    countries = alt.topo_feature(data.world_110m.url, 'countries')

    background=alt.Chart(countries).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        "equirectangular"
    ).properties(
        width=500,
        height=300
    )

    points = alt.Chart(mergedf).mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(10),
        tooltip='country'
    )

    chart=background + points
#    tooltip=xcol).interactive()
    return chart.to_html()

@app.callback(
    Output(component_id="hm_line", component_property="srcDoc"),
    #Output(component_id="cc_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
   # Input(component_id="home_tts", component_property="value"),
    Input(component_id="home_cts", component_property="value")
   # Input(component_id="countries", component_property="value"),
   # Input(component_id="years", component_property="value"),
   # Input(component_id="logistics_cc", component_property="value")    
)

def plot_line(countries, years, home_cts):
    print(countries, years, home_cts)
    arr=home_cts
    print("arr",type(arr))
    countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & 
                                                (bi['year'].isin(years)) & 
                                                (bi['Series Name']=="Cost of business start-up procedures (% of GNI per capita)") &
                                                (bi['value']<arr[1])]
    chart = alt.Chart(countries_years_series_filtered).mark_line(point=True).encode(
        alt.X('year:O',scale=alt.Scale(zero=False),title="check"),
        alt.Y('value:Q',scale=alt.Scale(zero=False)),
        color=alt.Color("Country Name:N",sort="ascending",legend=alt.Legend(title="Selected Countries")),
        tooltip='value')
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)