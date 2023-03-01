import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt

# loading the dataset
bi = pd.read_csv("datasets/melted_data.csv")

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
                    max=100,
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
    
                    ]),
                    # Resources Tab
                    dbc.Tab(label='Resources', children=[
                        dbc.Row([
                            html.H5("Financial Consideration")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H5("LINE CHART"),
                                html.Iframe(
                                    id='int_line',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                            ])   
                        ]),
                        dbc.Row([
                            html.H5("Non-Financial Consideration")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.H5("BAR CHART 1"),
                                html.Iframe(
                                    id='ur_bar',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                            ]),
                            dbc.Col([
                                html.H5("BAR CHART 2"),
                                html.Iframe(
                                    id='pr_bar',
                                    style={'border-width': '0', 'width': '100%', 'height': '400px'}
                                )
                            ])
                        ]) 
                    ]),
                    # Logistics Tab
                    dbc.Tab(label='Logistics', children=[
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

# callback for resources int_line
@app.callback(
    Output(component_id="int_line", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
)
def plot_int_line(countries, years):

    # countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & 
    #                                             (bi['year'].isin(years)) & 
    #                                             (bi['Series Name']=='Interest rate spread (lending rate minus deposit rate, %)')]
    
    # countries_years_series_filtered['year'] = pd.to_datetime(countries_years_series_filtered['year'], format='%Y')
    # print(countries_years_series_filtered.head())

    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name']=='Unemployment with advanced education (% of total labor force with advanced education)') & (bi['year'].isin(years))]
    df['year'] = pd.to_datetime(df['year'], format='%Y')

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('year:T'),
        y=alt.Y('value:Q', title='Interest Rate Spread (%)'),
        color='Country Name',
        tooltip=['Country Name', 'year', 'value']).properties( 
            height = 200,
            width = 700)
    
    chart2 = alt.Chart(df).mark_circle().encode(
        x=alt.X('year:T'),
        y=alt.Y('value:Q'),
        color='Country Name',
        tooltip=['Country Name', 'year', 'value'])

    chart3 = chart + chart2
    
    return chart3.to_html()


# callback for resources ur_bar
@app.callback(
    Output(component_id="ur_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
)

def plot_ur_bar(countries, years):
    series = ['Unemployment with advanced education (% of total labor force with advanced education)', 
          'Unemployment with basic education (% of total labor force with basic education)', 
          'Unemployment with intermediate education (% of total labor force with intermediate education)']

    bi['education_level'] = bi['Series Name'].str.extract('Unemployment with (\w+) education')
    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Country Name:N'),
        y=alt.Y('value:Q', title='% of Total Labor Force'),
        color='education_level',
        tooltip=['Country Name', 'year', 'value']).properties(  
        height = 400,
        width = 300
    ) 
    
    #add new column with just adnvanced education, basic etc...
    return chart.to_html()


# callback for resources pr_bar
@app.callback(
    Output(component_id="pr_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
)

def plot_ppr_bar(countries, years):
    series = ['Unemployment with advanced education (% of total labor force with advanced education)', 
          'Unemployment with basic education (% of total labor force with basic education)', 
          'Unemployment with intermediate education (% of total labor force with intermediate education)']

    bi['education_level'] = bi['Series Name'].str.extract('Unemployment with (\w+) education')
    df = bi[(bi['Country Name'].isin(countries)) & (bi['Series Name'].isin(series)) & (bi['year'].isin(years))]
    df['year'] = pd.to_datetime(df['year'], format='%Y')
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Country Name:N'),
        y=alt.Y('value:Q', title='% of Total Labor Force'),
        color='education_level',
        tooltip=['Country Name', 'year', 'value']).properties(  
        height = 400,
        width = 300
    ) 
    
    #add new column with just adnvanced education, basic etc...
    return chart.to_html()


if __name__ == '__main__':
    app.run_server(debug=False)