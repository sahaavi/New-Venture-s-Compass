import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt
from vega_datasets import data
import plotly.graph_objects as go
import math
from utils import resources_util as ru

# loading the dataset
bi = pd.read_csv("data/processed/melted_data.csv")
latlon = pd.read_csv("data/raw/world_country_and_usa_states_latitude_and_longitude_values.csv")
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
                "Cost to Start (%' of income per capita)'"
                ),
                dcc.RangeSlider(
                    id='home_cts',
                    min=0,
                    max=500,
                    value=[0, 500],
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
                    }
                )
            ]),
            # Time to Start Slider
            html.Div([
                html.Label(
                    "Time to Start (days)"
                ),
                dcc.RangeSlider(
                    id='home_tts',
                    min=0,
                    max=250,
                    value=[0, 250],
                    allowCross=False,
                    tooltip={
                        'placement':'bottom'
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
                        'placement':'bottom'
                    }
                )
            ]),
            html.Br(),
            html.H5("Logistics tab", style={"textAlign": "center"}),
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
            #Header across tabs
            html.H3("An Interactive Guide to select countries for establishing your new business", style={"textAlign": "center"}),
            html.Hr(),
            #Overview of the app
            dbc.Row([
                html.P('Hi there! Congratulations on thinking about starting a new business! \
                This dashboard is an interactive guide that helps to understand different aspects that are important in starting a business.'),
                html.P('In default mode, it shows data for 10 countries that are in World Bank database. \
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
                       value=['Canada', 'Argentina', 'Albania', 'Kenya', 'Thailand'],
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
                                    style={'border-width': '0', 'width': '100%', 'height': '250px'}
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
                                html.H5("Logistics Performance Index"),
                                dcc.Graph(id="lpi_radar", figure={})
                            ])
                        ]),
                        # end of 1st row for bar and radar chart
                        # 2nd row for horizontal stacked bar
                        dbc.Row([
                            html.H5("Time to Export (hours)"),
                            html.Iframe(
                                    id='tte_sb',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                        ]),
                        # 3rd row for horizontal stacked bar
                        dbc.Row([
                            html.H5("Time to Import (hours)"),
                            html.Iframe(
                                    id='tti_sb',
                                    style={'border-width': '0', 'width': '100%', 'height': '200px'}
                                )
                        ])
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
    Input(component_id="home_cts", component_property="value")
)

def plot_map(countries, years, home_cts):

    arr=home_cts
    if countries == None:

        df_hme = bi[(bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]

        df_hme = df_hme.iloc[0:10]

    else: 

        if years == None:
            df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]
        else:
            df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['year'].isin(years)) & (bi['value']<=arr[1])]

    df_hme['year'] = pd.to_datetime(df_hme['year'], format='%Y')

    mergedf=pd.merge(df_hme, latlon, how='left',left_on='Country Name',right_on='country')
    states_m = alt.topo_feature(data.us_10m.url, feature='states')
    countries = alt.topo_feature(data.world_110m.url, 'countries')

    background=alt.Chart(countries).mark_geoshape(
        fill='palegreen',
        stroke='white'
    ).project(
        "equirectangular"
    ).properties(
        width=700,
        height=200
    )
    
    points = alt.Chart(mergedf).mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(10),
        color='Country Name:N',
        tooltip='Country Name'
    )

    chart=(background + points)

    return chart.to_html()

@app.callback(
    Output(component_id="hm_line", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="home_cts", component_property="value")
)

def plot_line(countries, years, home_cts):
    arr=home_cts
    if countries == None:

        df_hme = bi[(bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]
        df_hme = df_hme.iloc[0:10]

    else: 

        if years == None:
            df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]
        else:
            df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['year'].isin(years)) & (bi['value']<=arr[1])]
    
    df_hme['year'] = pd.to_datetime(df_hme['year'], format='%Y')
    
    brush = alt.selection_interval()
    click = alt.selection_multi(fields=['Country Name'], bind='legend')
    
    cost_chart = alt.Chart(df_hme).mark_line(point=True).encode(
        alt.X('year:T',scale=alt.Scale(zero=False),title="Cost to implement business"),
        alt.Y('value:Q',title="% of GNI per capita"),
        tooltip='value:Q',
        color=alt.condition(brush, 'Country Name', alt.value('lightgray')),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))).add_selection(brush).properties(
        width=300,
        height=250)
        
    bi_2 = bi
    bi_2['year'] = pd.to_datetime(bi_2['year'], format='%Y')

    mergehmdf=pd.merge(df_hme, bi_2, how='left',on=['Country Name','year'])
    mergehmdf=mergehmdf[mergehmdf['Series Name_y']=='Time required to start a business (days)']
    mergehmdf['year'] = pd.to_datetime(mergehmdf['year'], format='%Y')
    time_chart = (alt.Chart(mergehmdf).mark_line(point=True).encode(
        alt.X('year:T',scale=alt.Scale(zero=False),title="Time to implement business"),
        alt.Y('value_y:Q',title="Time required to start a business (days)"),
        color='Country Name',
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        tooltip='value_y:Q').properties(
        width=300,
        height=250))
        
    chart = (cost_chart | time_chart).add_selection(click)
        
    return chart.to_html()

# --- RESOURCES CALLBACK --- 

# callback for resources int_line
@app.callback(
    Output(component_id="int_line", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id ="resources_air", component_property="value")
)

def plot_int_line(countries, years, interest_rate):

    series_name = 'Interest rate spread (lending rate minus deposit rate, %)'
    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']==series_name) & (bi['year'].isin(years))] 
    
    if interest_rate != None:

         selected_countries = ru.get_selected_countries(bi, countries, interest_rate)
         df = df[df['Country Name'].isin(selected_countries)]
    
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    chart = ru.create_interest_rate_chart(df)

    return chart.to_html()

# callback for resources ur_bar
@app.callback(
    Output(component_id="ur_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="resources_air", component_property="value")
)
def plot_ur_bar(countries, years, interest_rate):

    series = ['Unemployment with advanced education (% of total labor force with advanced education)', 
              'Unemployment with intermediate education (% of total labor force with intermediate education)',
              'Unemployment with basic education (% of total labor force with basic education)']

    bi['education_level'] = bi['Series Name'].str.extract('Unemployment with (\w+) education')

    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]

    if interest_rate != None:
        selected_countries = ru.get_selected_countries(bi, countries, interest_rate)
        df = bi[(bi['Country Name'].isin(selected_countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]
    
    chart = ru.create_unemployment_rate_chart(df)

    return chart.to_html()

# callback for resources pr_bar
@app.callback(
    Output(component_id="pr_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="resources_air", component_property="value")
)

def plot_pr_bar(countries, years, interest_rate):

    series_name = 'Labor force participation rate for ages 15-24, total (%) (national estimate)'
    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'] == series_name) & (bi['year'].isin(years))]

    if interest_rate != None:
        selected_countries = ru.get_selected_countries(bi, countries, interest_rate)
        df = bi[(bi['Country Name'].isin(selected_countries)) & (bi['Series Name']==series_name) & (bi['year'].isin(years))]
    
    chart = ru.create_participation_rate_chart(df)
    
    return chart.to_html()


# --- LOGISITICS CALLBACK ---
@app.callback(
    Output(component_id="cc_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_cc", component_property="value")
)

def plot_cc_bar(countries, years, logistics_cc):
    if countries == None:

        countries_years_series_filtered = bi[(bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]

        countries_years_series_filtered = countries_years_series_filtered.iloc[0:10]

    else: 

        if years == None:
            countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]
        else:
            countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & (bi['year'].isin(years)) & (bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]

    chart = alt.Chart(countries_years_series_filtered).mark_bar().encode(
        x=alt.X('Country Name', title=None),
        y=alt.Y('value', title='Days'),
        color='Country Name',
        column=alt.Column('year', title=None),
        tooltip=['Country Name', 'year', 'value'])
    return chart.to_html()

# callback for logistics lpi_radar
@app.callback(
    Output(component_id="lpi_radar", component_property="figure"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
)

def plot_lpi_radar(countries, years):
    max = math.ceil(bi[bi["Series Name"]=="Logistics performance index: Overall (1=low to 5=high)"]["value"].max())
    min = math.floor(bi[bi["Series Name"]=="Logistics performance index: Overall (1=low to 5=high)"]["value"].min())
    if countries == None:
        countries = ['Afghanistan','Albania','Algeria','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan']
    if years == None:
        years=['2014']
    fig = go.Figure()
    # tracing layout
    for i in countries:
        fig.add_trace(go.Scatterpolar(
        r=bi[(bi["Series Name"]=="Logistics performance index: Overall (1=low to 5=high)") &
        (bi["Country Name"]==i) &
        (bi["year"].isin(years))]["value"].values.tolist(),
        theta=years,
        fill='toself',
        name=i,
        connectgaps=True
    ))
    # each circle values
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[min, max]
        )),
    showlegend=False
    )
    return fig

# callback for logistics tte_sb & logistics tti_sb
@app.callback(
    Output(component_id="tte_sb", component_property="srcDoc"),
    [Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_tte", component_property="value"),
    Input(component_id="logistics_tti", component_property="value"),
    State('logistics_tte', 'value'),
    State('logistics_tti', 'value')]
    
)

def plot_tte_sb(countries, years, tte_hours, tti_hours, tte_state_value, tti_state_value):
    if tte_state_value is None:
        return 'Rangeslider not initialized yet'
    elif tti_state_value is None:
        return 'Rangeslider not initialized yet'
    else:
        click = alt.selection_multi(fields=['Country Name'], bind='legend')
        
        filtered_export_tte = bi[(bi['Country Name'].isin(countries)) & 
                        (bi['year'].isin(years)) & 
                        ((bi['Series Name'] == 'Time to export, border compliance (hours)') |
                        (bi['Series Name'] == 'Time to export, documentary compliance (hours)')) & 
                        (bi['value'] >= tte_hours[0]) & 
                        (bi['value'] <= tte_hours[1])]
        
        tte_chart = alt.Chart(filtered_export_tte).mark_bar(orient='horizontal').encode(
            y=alt.Y('year', title=None),
            x=alt.X('value', title=None),
            color='Country Name',
            row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
            tooltip=['Country Name', 'year', 'value'],
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
        ).properties( 
                height = 100,
                width = 300)

        filtered_export_tti = bi[(bi['Country Name'].isin(countries)) & 
                        (bi['year'].isin(years)) & 
                        ((bi['Series Name'] == 'Time to import, border compliance (hours)') |
                        (bi['Series Name'] == 'Time to import, documentary compliance (hours)')) & 
                        (bi['value'] >= tti_hours[0]) & 
                        (bi['value'] <= tti_hours[1])]
        
        tti_chart = alt.Chart(filtered_export_tti).mark_bar(orient='horizontal').encode(
            y=alt.Y('year', title=None),
            x=alt.X('value', title=None),
            color='Country Name',
            row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
            tooltip=['Country Name', 'year', 'value'],
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
        ).properties( 
                height = 100,
                width = 300)

    chart = (tte_chart & tti_chart).add_selection(click)
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=False)