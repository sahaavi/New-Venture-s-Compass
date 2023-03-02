import math
import pandas as pd
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import altair as alt
import plotly.graph_objects as go

# loading the dataset
bi = pd.read_csv("datasets/melted_data.csv")
bi['year'] = bi['year'].astype(str)

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
                    value=[30, 60],
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
                'Time to Import (hours)'
                ),
                dcc.RangeSlider(
                    id='logistics_tti',
                    min=0,
                    max=200,
                    value=[40, 70],
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
                # top filters country's coloumn
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
                # top filters year's coloumn
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
                # end of top filters year's coloumn
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
                        
                    ]),
                    # Logistics Tab
                    dbc.Tab(label='Logistics', children=[
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

# callback for logistics cc_bar
@app.callback(
    Output(component_id="cc_bar", component_property="srcDoc"),
    Input(component_id="countries", component_property="value"),
    Input(component_id="years", component_property="value"),
    Input(component_id="logistics_cc", component_property="value")
)

def plot_cc_bar(countries, years, logistics_cc):
    countries_years_series_filtered = bi[(bi['Country Name'].isin(countries)) & 
                                                (bi['year'].isin(years)) & 
                                                (bi['Series Name']=="Average time to clear exports through customs (days)") & 
                                                (bi['value']<logistics_cc)]
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
    app.run_server(debug=True)