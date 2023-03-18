import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt
from vega_datasets import data
import math
from utils import app_charts as ac, app_utils as au

# loading the dataset
bi = pd.read_csv("../data/processed/melted_data.csv")
latlon = pd.read_csv("../data/raw/world_country_and_usa_states_latitude_and_longitude_values.csv")
bi['year'] = bi['year'].astype(str)

selected_countries = None

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    #app header
    dbc.Row([
    html.H1("New Venture(s) Compass", style={"textAlign": "center"}),
    html.Hr(),
    ]),
    # filters row
    dbc.Row([
        # side filter column
        dbc.Col([
            html.Br(),
            html.H4('Filters & Controls'),
            html.Hr(),
            #Home tab sliders
            html.Br(),
            html.H5("Home tab", style={"textAlign": "center"}),
            html.Br(),
            # Cost to Start Slider
            
            html.Div([
                html.Label(
                "Average Cost to Start (% of income per capita)"
                ),
                dcc.RangeSlider(
                    id='home_cts',
                    min=0,
                    max=50,
                    value=[0, 50],
                    allowCross=False,
                    tooltip={
                        'placement':'bottom',
                        'always_visible': True
                    }
                )
            ]),
            # Time to Start Slider
            html.Div([
                html.Label(
                    "Average Time to Start (days)"
                ),
                dcc.RangeSlider(
                    id='home_tts',
                    min=0,
                    max=50,
                    value=[0, 50],
                    allowCross=False,
                    tooltip={
                        'placement':'bottom',
                        'always_visible': True
                    }
                )
            ]),
            #Resources tab sliders
            html.Br(),
            html.H5("Resources tab", style={"textAlign": "center"}),
            html.Br(),
            # Average Interest Rate Slider
            html.Div([
                html.Label(
                'Average Interest Rate Spread (%)'
                ),
                dcc.RangeSlider(
                    id='resources_air',
                    min=0,
                    max=15,
                    allowCross=False,
                    tooltip={
                        'placement':'bottom',
                        'always_visible': True
                    }
                )
            ]),
            html.Br(),
            html.H5("Logistics tab", style={"textAlign": "center"}),
            html.Br(),
            # Time to Export Slider
            html.Div([
                html.Label(
                'Average Time to Export (hours)'
                ),
                dcc.RangeSlider(
                    id='logistics_tte',
                    min=0,
                    max=1200,
                    value=[0, 1200],
                    allowCross=False,
                    tooltip={
                        'placement':'bottom',
                        'always_visible': True
                    }
                )
            ]),
            # Time to Import Slider
            html.Div([
                html.Label(
                'Average Time to Import (hours)'
                ),
                dcc.RangeSlider(
                    id='logistics_tti',
                    min=0,
                    max=1200,
                    value=[0, 1200],
                    allowCross=False,
                    tooltip={
                        'placement':'bottom',
                        'always_visible': True
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
                    value=30
                )
            ]),
        ], 
        md=3,
        style={'border': '1px solid #d3d3d3', 'border-radius': '10px'}
        ),
        # end of side filter column
        # tabs column
        dbc.Col([
            #Header across tabs
            html.H3("An Interactive Guide to select countries for establishing your new business", style={"textAlign": "center"}),
            html.Hr(),
            #Overview of the app
            dbc.Row([
                html.P('Hi there! Congratulations on thinking about starting a new business! \
                This dashboard is an interactive guide that helps to understand different aspects that are important in starting a business.'),
                html.P('In default mode, data for 6 countries is shown, with each country randomly chosen from a different continent (excluding Antarctica) using the World Bank database. \
                We recommend to start browsing through the tabs to get an idea of different aspects. \
                Once finished, you can choose years and countries for your own assessment, Remember, both inputs are mandatory. \
                Sliders are present on the side to further fine tune your selection for each tab. \
                ')
            ]),
            # top filters row
            dbc.Row([
                # top filters portion
                dbc.Col(
                    # dropdown for country
                    dcc.Dropdown(
                        id='countries',
                        placeholder='Select countries...',
                       value=['Canada', 'Argentina', 'Albania', 'Kenya', 'Thailand', 'Australia'],
                    #    value=['All'],
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
                        value=['2014','2015','2016','2017','2018','2019'],
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
                #html.P('With a help paragraph'),
                # tabs
                dbc.Tabs(id='tabs', children=[
                    # Home Tab
                    dbc.Tab(label='Home', children=[
                        dbc.Row([
                            html.H5("Geographic Location")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.P('Understanding the geographic location of the country is very important. This helps to know the neighboring countries, ports etc.'), 
                                html.Iframe(
                                    id='hm_map',
                                    style={'border-width': '0', 'width': '100%', 'height': '300px'}
                                )
                            ])   
                        ]),
                        dbc.Row([
                            html.H5("Cost and Time requirements to start a business"),
                            html.P("Cost and time factors are very important. Cost tells us how costly interms of a countrie's % of income per capita \
                                    is required to start a business in the country. Time tells us how many days are required in business starting procedures. \
                                    Lower the percentage and days, favorable it is for anyone to start a business.")
                        ]),
                       dbc.Row([
                            dbc.Col([
                                html.Iframe(
                                    id='hm_line',
                                    style={'border-width': '0', 'width': '100%', 'height': '350px'}
                                )
                            ])
                        ])                        
                    ]),
                    # end of home tab
                    # Resources Tab
                    dbc.Tab(label='Resources', children=[
                        dbc.Row([
                            html.H5("Financial Consideration"),
                            html.P("As the next step, we think about knowledge of different resources available or necessary for the business and their supply and demand. \
                                    First is the finance or credit related information.")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H6("Tracking Interest Rate Spread: Lending Rate Minus Deposit Rate (%)"),
                                html.Iframe(
                                    id='int_line',
                                    style={'border-width': '0', 'width': '100%', 'height': '250px'}
                                )
                            ])   
                        ]),
                        dbc.Row([
                            html.H5("Non-Financial Consideration"),
                            html.P("Other type of resources available or necessary for the business is labor related. Information regarding them is provided below.")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H6("Unemployment Rates between Labor Force with Basic, Intermediate, and Advanced Education"),
                                html.Iframe(
                                    id='ur_bar',
                                    style={'border-width': '0', 'width': '100%', 'height': '350px'}
                                )
                            ]),
                            dbc.Col([
                                html.H6("National Estimate of Total Labour Force Participation Rate for Ages 15-24"),
                                html.Iframe(
                                    id='pr_bar',
                                    style={'border-width': '0', 'width': '100%', 'height': '350px'}
                                )
                            ])
                        ],className="g-0") 
                    ]),
                    # Logistics Tab
                    dbc.Tab(label='Logistics', children=[
                        dbc.Row([
                            html.H5("Imports and Exports"),
                            html.P("Logistics of how easy and quick it is to import and export and clear customs? Information regarding them is provided below \
                                    which marks the final items to consider.")
                        ]),
                        # 1st row for bar and radar chart
                        dbc.Row([
                            # multi-bar chart
                            dbc.Col([
                                html.H5("Average time to clear Exports through customs (days)"),
                                html.Iframe(
                                    id='cc_bar',
                                    style={'border-width': '0', 'width': '100%', 'height': '500px'}
                                )
                            ]),
                            # radar chart
                            dbc.Col([
                                html.H5("Logistics Performance Index", style={"text-align": "center"}),
                                dcc.Graph(id="lpi_radar", figure={})
                            ])
                        ]),
                        # end of 1st row for bar and radar chart
                        # 2nd row for horizontal stacked bar
                        dbc.Row([
                            html.H5("Time to Export/Import (hours)"),
                            html.Iframe(
                                    id='tte_sb',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                        ]),
                    ])
                    # end of logistics tab                               
                ])
                # end of tabs
            ])
            # end of tabs row
        ])
        # end of tabs column
    ])
    # end of filters row
])

# --- HOME CALLBACK ---

@app.callback(
    Output(component_id="hm_map", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value")
)

def plot_map(countries, years, home_cts, home_tts, resources_air, logistics_cc, logistics_tte, logistics_tti):
    
    logistics_cc = [0, logistics_cc]
    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    #intersection of countries after all filters applied
    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)

    df_hme = bi[(bi['Country Name'].isin(selected_countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['year'].isin(years))]
    df_hme.loc[:, 'year'] = pd.to_datetime(df_hme['year'], format='%Y')

    countries = alt.topo_feature(data.world_110m.url, 'countries')
    mergedf=pd.merge(df_hme, latlon, how='left',left_on='Country Name',right_on='country')

    map = ac.create_map_chart(countries, mergedf)
    return map.to_html()

@app.callback(
    Output(component_id="hm_line", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value")
)

def plot_line(countries, years, home_cts, home_tts, resources_air, logistics_cc, logistics_tte, logistics_tti):

    logistics_cc = [0, logistics_cc]
    series_name_cts = 'Cost of business start-up procedures (% of GNI per capita)'
    df_cts = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']== series_name_cts) & (bi['year'].isin(years))]
    df_cts.loc[:, 'year'] = pd.to_datetime(df_cts['year'], format='%Y')

    series_name_tts = 'Time required to start a business (days)'
    df_tts = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']== series_name_tts) & (bi['year'].isin(years))]
    df_tts.loc[:, 'year'] = pd.to_datetime(df_tts['year'], format='%Y')

    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)

    # filer both dataframes using the selected_countries
    df_cts = df_cts[df_cts['Country Name'].isin(selected_countries)]
    df_tts = df_tts[df_tts['Country Name'].isin(selected_countries)]
        
    chart = ac.create_tts_cts_charts(df_cts, df_tts)
    return chart.to_html()

# --- RESOURCES CALLBACK --- 

# callback for resources int_line

@app.callback(
    Output(component_id="int_line", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value")
)

def plot_int_line(countries, years, home_cts, home_tts, resources_air, logistics_cc, logistics_tte, logistics_tti):

    logistics_cc = [0, logistics_cc]
    series_name = 'Interest rate spread (lending rate minus deposit rate, %)'

    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']==series_name) & (bi['year'].isin(years))] 
    df.loc[:, 'year'] = pd.to_datetime(df['year'], format='%Y')
    
    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)
    df = df[df['Country Name'].isin(selected_countries)]
    
    chart = ac.create_interest_rate_chart(df)
    return chart.to_html()

# callback for resources ur_bar
@app.callback(
    Output(component_id="ur_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value")

)
def plot_ur_bar(countries, years, home_cts, home_tts, resources_air, logistics_cc, logistics_tte, logistics_tti):

    logistics_cc = [0, logistics_cc]
    series = ['Unemployment with advanced education (% of total labor force with advanced education)', 
              'Unemployment with intermediate education (% of total labor force with intermediate education)',
              'Unemployment with basic education (% of total labor force with basic education)']

    bi['education_level'] = bi['Series Name'].str.extract('Unemployment with (\w+) education')
    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]

    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)
    df = df[df['Country Name'].isin(selected_countries)]
    
    chart = ac.create_unemployment_rate_chart(df)
    return chart.to_html()

# callback for resources pr_bar
@app.callback(
    Output(component_id="pr_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value")
)

def plot_pr_bar(countries, years, home_cts, home_tts, resources_air, logistics_cc, logistics_tte, logistics_tti):
    
    logistics_cc = [0, logistics_cc]
    series_name = 'Labor force participation rate for ages 15-24, total (%) (national estimate)'
    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'] == series_name) & (bi['year'].isin(years))]
    df.loc[:, 'year'] = pd.to_datetime(df['year'], format='%Y')
    
    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)
    df = df[df['Country Name'].isin(selected_countries)]

    chart = ac.create_participation_rate_chart(df)
    return chart.to_html()

# --- LOGISITICS CALLBACK ---

# callback for logistics cc_bar
@app.callback(
    Output(component_id="cc_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value")
)

def plot_cc_bar(countries, years, logistics_cc, logistics_tte, logistics_tti, home_cts, home_tts, resources_air):

    logistics_cc = [0, logistics_cc]
    df = bi[(bi['Country Name'].isin(countries)) & 
            (bi['year'].isin(years)) & 
            (bi['Series Name']=="Average time to clear exports through customs (days)")]
    
    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)
    df = df[df['Country Name'].isin(selected_countries)]

    chart = ac.create_average_export_Clear_time(df)
    return chart.to_html()

# callback for logistics lpi_radar
@app.callback(
    Output(component_id="lpi_radar", component_property="figure"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value")
)

def plot_lpi_radar(countries, years, logistics_cc, logistics_tte, logistics_tti, home_cts, home_tts, resources_air):

    logistics_cc = [0, logistics_cc]
    max = math.ceil(bi[bi["Series Name"]=="Logistics performance index: Overall (1=low to 5=high)"]["value"].max())
    min = math.floor(bi[bi["Series Name"]=="Logistics performance index: Overall (1=low to 5=high)"]["value"].min())

    df = bi[(bi['Country Name'].isin(countries)) & 
            (bi['year'].isin(years)) & 
            (bi['Series Name']=="Logistics performance index: Overall (1=low to 5=high)")]

    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)
    df = df[df['Country Name'].isin(selected_countries)]

    fig = ac.create_logistics_performance_chart(df, max, min)
    return fig

# callback for logistics tte_sb & logistics tti_sb
@app.callback(
    Output(component_id="tte_sb", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_cc", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value"),
    Input(component_id="home_cts", component_property="value"),
    Input(component_id="home_tts", component_property="value"),
    Input(component_id ="resources_air", component_property="value")
)

def plot_tte_sb(countries, years, logistics_cc, logistics_tte, logistics_tti, home_cts, home_tts, resources_air):
    
    logistics_cc = [0, logistics_cc]
    
    df_tte = bi[(bi['Country Name'].isin(countries)) & 
                (bi['year'].isin(years)) & 
                ((bi['Series Name'] == 'Time to export, border compliance (hours)') |
                (bi['Series Name'] == 'Time to export, documentary compliance (hours)'))]
    
    df_tti = bi[(bi['Country Name'].isin(countries)) & 
                (bi['year'].isin(years)) & 
                ((bi['Series Name'] == 'Time to import, border compliance (hours)') |
                (bi['Series Name'] == 'Time to import, documentary compliance (hours)'))]
    
    sliders_series = [
        (home_cts, 'Cost of business start-up procedures (% of GNI per capita)'),
        (home_tts, 'Time required to start a business (days)'),
        (resources_air, 'Interest rate spread (lending rate minus deposit rate, %)'),
        (logistics_cc, 'Average time to clear exports through customs (days)') ,
        (logistics_tte, 'Time to export, border compliance (hours)'),
        (logistics_tte, 'Time to export, documentary compliance (hours)'),
        (logistics_tti, 'Time to import, border compliance (hours)'),
        (logistics_tti, 'Time to import, documentary compliance (hours)')
    ]

    selected_countries = au.get_countries_based_on_sliders(bi, countries, sliders_series)
    df_tte = df_tte[df_tte['Country Name'].isin(selected_countries)]
    df_tti = df_tti[df_tti['Country Name'].isin(selected_countries)]

    
    chart = ac.create_time_export_import_chart(df_tte, df_tti)
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=False)
