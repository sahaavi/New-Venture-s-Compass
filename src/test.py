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
bi = pd.read_csv("data/processed/melted_data.csv")
bi['year'] = bi['year'].astype(str)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        
        html.H5("Time to Export (hours)"),
        html.Iframe(
                id='tte_sb',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}
            ),
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
                        
    ])
])


@app.callback(
    Output(component_id="tte_sb", component_property="srcDoc"),
    Input(component_id="years", component_property="value")
)

def plot_tte_sb(years):
    
    # if tte_state_value is None:
    #     return 'Rangeslider not initialized yet'
    # elif tti_state_value is None:
    #     return 'Rangeslider not initialized yet'
    # else:
    # brush = alt.selection_interval()
    click = alt.selection_multi(fields=['Country Name'], bind='legend')

    countries = ["Albania", "India", "Afghanistan", "Qatar", "Canada"]
    tte_hours = [5, 20]
    tti_hours = [5, 20]
    
    filtered_export_tte = bi[(bi['Country Name'].isin(countries)) & 
                    (bi['year'].isin(years)) & 
                    ((bi['Series Name'] == 'Time to export, border compliance (hours)') |
                    (bi['Series Name'] == 'Time to export, documentary compliance (hours)')) & 
                    (bi['value'] >= tte_hours[0]) & 
                    (bi['value'] <= tte_hours[1])]
    
    tte_chart = alt.Chart(filtered_export_tte).mark_bar(orient='horizontal').encode(
        y=alt.Y('year', title=None),
        x=alt.X('value', title='Days'),
        color='Country Name',
        row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    )

    filtered_export_tti = bi[(bi['Country Name'].isin(countries)) & 
                    (bi['year'].isin(years)) & 
                    ((bi['Series Name'] == 'Time to import, border compliance (hours)') |
                    (bi['Series Name'] == 'Time to import, documentary compliance (hours)')) & 
                    (bi['value'] >= tti_hours[0]) & 
                    (bi['value'] <= tti_hours[1])]
    
    tti_chart = alt.Chart(filtered_export_tti).mark_bar(orient='horizontal').encode(
        y=alt.Y('year', title=None),
        x=alt.X('value', title='Days'),
        color='Country Name',
        row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    )
    
    chart = (tte_chart & tti_chart).add_selection(click)
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)