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

# loading the dataset
bi = pd.read_csv("../data/processed/melted_data.csv")
latlon = pd.read_csv("../data/raw/world_country_and_usa_states_latitude_and_longitude_values.csv")
bi['year'] = bi['year'].astype(str)

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
                html.P('In default mode, it shows data for 10 countries that are in World Bank datase. \
                We recommend to start browsing through the tabs to get an idea of different aspects. \
                Once finished, you can choose years and countries for your own assessment, Remember, both inputs are mandatory. \
                Sliders are present on the side to further fine tune your selection. \
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
#                        value=['Canada','United States','Mexico'],
#                        value=['All'],
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
                        #value=['2014','2015','2016','2017','2018','2019'],
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


## callback for home tab start
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
    #print(home_tts)
    arr=home_cts
    #arr2=home_tts
    print("map",years)
    if countries == None:
    #default/first view - All countries and years
        #print("selected/default countries")
        df_hme = bi[(bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]
        #df_ctrl2 = bi[(bi['Series Name']=='Time required to start a business (days)') & (bi['value']<arr2[1]) & (bi['value']>arr2[0])]
        #df_hme = pd.merge(df_ctrl1, df_ctrl2)
        df_hme = df_hme.iloc[0:10]
        #print("newdf2")
        #print(df_hme)
        #countries = df_hme['Country Name'].tolist()
        print("default end")
    else: 
    #data input for selected countries
        print("selected/default countries",countries,years)
        if years == None:
            df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]
        else:
            df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['year'].isin(years)) & (bi['value']<=arr[1])]
        #df_ctrl2 = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Time required to start a business (days)') & (bi['year'].isin(years)) & (bi['value']<arr2[1]) &  (bi['value']>arr2[0])]
        #df_hme=pd.merge(df_ctrl1, df_ctrl2)
    df_hme['year'] = pd.to_datetime(df_hme['year'], format='%Y')
    print("pdmerge")
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
#    tooltip=xcol).interactive()
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
    #default/first view - All countries and years
        print("selected/default countries")
        df_hme = bi[(bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['value']<=arr[1])]
        df_hme = df_hme.iloc[0:10]
        print("View fine",df_hme)
        #countries = df_hme['Country Name'].tolist()
        print("default end")
    else: 
    #data input for selected countries
        print("selected/default countries",years)
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
        
    #df_hme = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Cost of business start-up procedures (% of GNI per capita)') & (bi['year'].isin(years)) & (bi['value']<arr[1])]
    bi_2 = bi
    bi_2['year'] = pd.to_datetime(bi_2['year'], format='%Y')
    #mergehmdf=pd.concat([df_hme, bi],join='inner',keys=['Country Name','year'])
    
    mergehmdf=pd.merge(df_hme, bi_2, how='left',on=['Country Name','year'])
    mergehmdf=mergehmdf[mergehmdf['Series Name_y']=='Time required to start a business (days)']
    print("final",mergehmdf)
    mergehmdf['year'] = pd.to_datetime(mergehmdf['year'], format='%Y')
    #mergehmdf=mergehmdf.reset_index()
    time_chart = (alt.Chart(mergehmdf).mark_line(point=True).encode(
        alt.X('year:T',scale=alt.Scale(zero=False),title="Time to implement business"),
        alt.Y('value_y:Q',title="Time required to start a business (days)"),
        #color=alt.Color("Country Name:N",sort="ascending",legend=alt.Legend(title="Selected Countries")),
        color='Country Name',
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        tooltip='value_y:Q').properties(
        width=300,
        height=250))
        
    chart = (cost_chart | time_chart).add_selection(click)
        
    return chart.to_html()
##home tab callback end

##Resources tab callback start
# callback for resources int_line
@app.callback(
    Output(component_id="int_line", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value")
    #Input(component_id="home_cts", component_property="value")
)
def plot_int_line(countries, years):
    #arr=home_cts
    # countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & 
    #                                             (bi['year'].isin(years)) & 
    #                                             (bi['Series Name']=='Interest rate spread (lending rate minus deposit rate, %)')]
    
    # countries_years_series_filtered['year'] = pd.to_datetime(countries_years_series_filtered['year'], format='%Y')
    # print(countries_years_series_filtered.head())

    if countries == None:
    #default/first view - All countries and years
        print("selected/default countries")

        df = bi[(bi['Series Name']=='Unemployment with advanced education (% of total labor force with advanced education)')]
        df = df.iloc[0:10]
        print(df)
        #countries = df_hme['Country Name'].tolist()
        print("default end -t2")
    else: 
    #data input for selected countries
        if years == None:
            df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Unemployment with advanced education (% of total labor force with advanced education)')]
        else:
            print("selected/default countries",years)
            df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Unemployment with advanced education (% of total labor force with advanced education)') & (bi['year'].isin(years))]    

    #df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Unemployment with advanced education (% of total labor force with advanced education)') & (bi['year'].isin(years))]


    df['year'] = pd.to_datetime(df['year'], format='%Y')

    chart1 = alt.Chart(df).mark_line().encode(
        x=alt.X('year:T' ),
        y=alt.Y('value:Q', title="Interest Rate Spread"),
        color='Country Name',
        tooltip=['Country Name', 'year', 'value']).properties( 
            height = 200,
            width = 700)
    
    chart2 = alt.Chart(df).mark_circle().encode(
        x=alt.X('year:T'),
        y=alt.Y('value:Q'),
        color='Country Name',
        tooltip=['Country Name', 'year', 'value'])

    chart_final = chart1 + chart2
    
    return chart_final.to_html()


# callback for resources ur_bar
@app.callback(
    Output(component_id="ur_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    #Input(component_id="home_cts", component_property="value")
)
def plot_ur_bar(countries, years):
    #arr=home_cts
    series = ['Unemployment with advanced education (% of total labor force with advanced education)', 
          'Unemployment with basic education (% of total labor force with basic education)', 
          'Unemployment with intermediate education (% of total labor force with intermediate education)']

    bi['education_level'] = bi['Series Name'].str.extract('Unemployment with (\w+) education')
    if countries == None:
    #default/first view - All countries and years
        print("selected/default countries")
        df = bi[(bi['Series Name'].isin(series))]
        df = df.iloc[0:10]
        print(df)
        #countries = df_hme['Country Name'].tolist()
        print("default end -t2")
    else:
        if years == None:
                df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series))]
        else:
            #data input for selected countries
            print("selected/default countries",years)
            df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]
    #df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Country Name:N', title="Country"),
        y=alt.Y('value:Q', title="Unemployment Rate"),
        color='education_level',
        tooltip=['Country Name', 'year', 'value']).properties(  
        height = 300,
        width = 300
    ) 
    
    #add new column with just adnvanced education, basic etc...
    return chart.to_html()


# callback for resources pr_bar
@app.callback(
    Output(component_id="pr_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value")
    #Input(component_id="home_cts", component_property="value")
)

def plot_pr_bar(countries, years):
    #arr=home_cts
    series_name = 'Labor force participation rate for ages 15-24, total (%) (national estimate)'
    if countries == None:
    #default/first view - All countries and years
        print("selected/default countries")
        df = bi[(bi['Series Name'] == series_name)]
        df = df.iloc[0:10]
        print(df)
        #countries = df_hme['Country Name'].tolist()
        print("default end -t2")
    else: 
        if years == None:
            df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'] == series_name)] 
        else:
            df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'] == series_name) & (bi['year'].isin(years))]
    
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    df.head()
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('value:Q', title="Participation Rate"),
        y=alt.Y('Country Name:N', title="Country"),
        color='Country Name',
        tooltip=['Country Name', 'year', 'value']).properties(  
        height = 300,
        width = 300
    ) 
    
    return chart.to_html()
## Resource tab callback end

## Logistics tab callback start
@app.callback(
    Output(component_id="cc_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_cc", component_property="value")
)

def plot_cc_bar(countries, years, logistics_cc):
    if countries == None:
    #default/first view - All countries and years
        #print("selected/default countries")
        countries_years_series_filtered = bi[(bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]
        #df_ctrl2 = bi[(bi['Series Name']=='Time required to start a business (days)') & (bi['value']<arr2[1]) & (bi['value']>arr2[0])]
        #df_hme = pd.merge(df_ctrl1, df_ctrl2)
        countries_years_series_filtered = countries_years_series_filtered.iloc[0:10]
        #print("newdf2")
        #print(df_hme)
        #countries = df_hme['Country Name'].tolist()
        print("default end")
    else: 
    #data input for selected countries
        #print("selected/default countries",countries,years)
        if years == None:
            countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]
        else:
            countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & (bi['year'].isin(years)) & (bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]

    #countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & (bi['year'].isin(years)) & (bi['Series Name']=="Average time to clear exports through customs (days)") & (bi['value']<logistics_cc)]
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

# callback for logistics tte_sb
@app.callback(
    Output(component_id="tte_sb", component_property="srcDoc"),
    [Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_tte", component_property="value")],
    State('logistics_tte', 'value')
)

def plot_tte_sb(countries, years, hours, state_value):
    if countries == None:
        countries = ['Afghanistan','Albania','Algeria','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan']
    if years == None:
        years=['2014']
    if hours == None:
        hours=[0,50]
    if state_value is None:
        return 'Rangeslider not initialized yet'
    else:
        filtered_export = bi[(bi['Country Name'].isin(countries)) & 
                        (bi['year'].isin(years)) & 
                        ((bi['Series Name'] == 'Time to export, border compliance (hours)') |
                        (bi['Series Name'] == 'Time to export, documentary compliance (hours)')) & 
                        (bi['value'] >= hours[0]) & 
                        (bi['value'] <= hours[1])]
        chart = alt.Chart(filtered_export).mark_bar(orient='horizontal').encode(
            y=alt.Y('year', title=None),
            x=alt.X('value', title='Days'),
            color='Country Name',
            row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
            tooltip=['Country Name', 'year', 'value'],
        )
        return chart.to_html()
    
# callback for logistics tti_sb
@app.callback(
    Output(component_id="tti_sb", component_property="srcDoc"),
    [Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_tti", component_property="value")],
    State('logistics_tte', 'value')
)

def plot_tte_sb(countries, years, hours, state_value):
    if countries == None:
        countries = ['Afghanistan','Albania','Algeria','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan']
    if years == None:
        years=['2014']
    if hours == None:
        hours=[0,50]
    if state_value is None:
        return 'Rangeslider not initialized yet'
    else:
        filtered_export = bi[(bi['Country Name'].isin(countries)) & 
                        (bi['year'].isin(years)) & 
                        ((bi['Series Name'] == 'Time to import, border compliance (hours)') |
                        (bi['Series Name'] == 'Time to import, documentary compliance (hours)')) & 
                        (bi['value'] >= hours[0]) & 
                        (bi['value'] <= hours[1])]
        chart = alt.Chart(filtered_export).mark_bar(orient='horizontal').encode(
            y=alt.Y('year', title=None),
            x=alt.X('value', title='Days'),
            color='Country Name',
            row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
            tooltip=['Country Name', 'year', 'value'],
        )
        return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=False)