import altair as alt
import plotly.graph_objects as go

def create_tts_cts_charts(df_cts, df_tts):
    """
    Create side-by-side Altair charts based on the given dataframes.

    Parameters:
    df_cts (pd.DataFrame): Dataframe containing data for the Cost to implement business chart
    df_tts (pd.DataFrame): Dataframe containing data for the Time to implement business chart

    Returns:
    alt.Chart: Combined Altair chart object
    """
    brush = alt.selection_interval()
    click = alt.selection_multi(fields=['Country Name'], bind='legend')

    cost_chart = alt.Chart(df_cts).mark_line(point=True).encode(
        alt.X('year:T', scale=alt.Scale(zero=False), title=None),
        alt.Y('value:Q', title="% of GNI per capita"),
        tooltip=['Country Name', 'year', 'value'],
        color=alt.condition(brush, 'Country Name', alt.value('lightgray')),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).add_selection(brush).properties(
        width=350,
        height=250,
        title={"text": "Cost to Implement Business", "fontSize": 14, "fontWeight": "bold", "anchor": "middle"}
    )

    time_chart = (alt.Chart(df_tts).mark_line(point=True).encode(
        alt.X('year:T', scale=alt.Scale(zero=False), title=None),
        alt.Y('value:Q', title="Time required to start a business (days)"),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        tooltip=['Country Name', 'year', 'value']
    ).properties(
        width=350,
        height=250,
        title={"text": "Time to Implement Business", "fontSize": 14, "fontWeight": "bold", "anchor": "middle"}
    ))

    chart = (cost_chart | time_chart).add_selection(click).configure(background='DarkKhaki')

    return chart



def create_map_chart(countries, mergedf):
    """
    Create an Altair map chart with points based on the given dataframes.

    Parameters:
    countries (pd.DataFrame): Dataframe containing country geographic information
    mergedf (pd.DataFrame): Dataframe containing data for the points on the map

    Returns:
    alt.Chart: Combined Altair chart object
    """
    background = alt.Chart(countries).mark_geoshape(
        fill='mintcream',
        stroke='lightgray'
    ).project(
        "equirectangular"
    ).properties(
        width=800,
        height=350
    )

    points = alt.Chart(mergedf).mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(35),
        color='Country Name:N',
        tooltip='Country Name'
    )

    chart = (background + points).configure_legend(title=None).configure(background='darkkhaki')

    return chart


def create_interest_rate_chart(df):
    """
    Create an Altair line chart for interest rate spread by country and year.

    Args:
        df (pd.DataFrame): A data frame containing columns 'year', 'value', and 'Country Name'.

    Returns:
        alt.Chart: An Altair line chart showing interest rate spread by country and year.
    """
    click = alt.selection_multi(fields=['Country Name'], bind='legend')
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('year:T', scale=alt.Scale(zero=False), title=None),
        y=alt.Y('value:Q', title="Interest Rate Spread", axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).properties(
        height=190,
        width=700
    ).configure(background='darkkhaki')
    return chart.add_selection(click)


def create_unemployment_rate_chart(df):
    """
    Create an Altair bar chart for unemployment rate by country, year, and education level.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', 'value', and 'education_level'.

    Returns:
        alt.Chart: An Altair bar chart showing unemployment rate by country, year, and education level.
    """
    click = alt.selection_multi(fields=['Country Name'], bind='legend')

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('education_level:N', title=None, axis=alt.Axis(labels=False, ticks=False)),
        y=alt.Y('value:Q', title="Unemployment Rate", axis=alt.Axis(titleFontSize=14)),
        color=alt.Color('education_level:N', legend=alt.Legend(title='Education Level', orient='bottom', columns=len(df['education_level'].unique()))),
        column=alt.Column('Country Name:N', title=None),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).properties(
        height=250,
        width=330
    ).configure_view(
        stroke='transparent'
    ).configure(background='darkkhaki')

    return chart.add_selection(click)


def create_participation_rate_chart(df):
    """
    Create an Altair bar chart for participation rate by country and year.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', and 'value'.

    Returns:
        alt.Chart: An Altair bar chart showing participation rate by country and year.
    """
    click = alt.selection_multi(fields=['Country Name'], bind='legend')

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('value:Q', title="Participation Rate", axis=alt.Axis(titleFontSize=14)),
        y=alt.Y('Country Name:N', title=None),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).properties(
        height=285,
        width=290
    ).configure(background='darkkhaki')

    return chart.add_selection(click)


def create_average_export_Clear_time(df):
    """
    Create an Altair vertical grouped bar chart for Average time to clear Exports through customs (days) by country and year.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', and 'value'.

    Returns:
        alt.Chart: An Altair bar chart showing Average time to clear Exports through customs (days) by country and year.
    """
    df = df[df['value'] != 0]

    click = alt.selection_multi(fields=['Country Name'], bind='legend')

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Country Name', title=None, axis=None),
        y=alt.Y('value', title='Days'),
        color='Country Name',
        column=alt.Column('year', title=None),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).properties(
        height=290,
        width=200).configure_legend(title=None).configure(background='darkkhaki')

    chart = (chart).add_selection(click)
    return chart

def create_time_export_import_chart(df_tte, df_tti):
    """
    Create an Altair horizontal multi grouped bar chart for Time to Export and Time to Import by country and year.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', and 'value'.

    Returns:
        alt.Chart: An Altair bar chart showing Time to Export and Time to Import by country and year.
    """
    click = alt.selection_multi(fields=['Country Name'], bind='legend')

    tte_chart = alt.Chart(df_tte).mark_bar(orient='horizontal').encode(
        y=alt.Y('year', title=None),
        x=alt.X('value', title=None),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        column=alt.Column('Series Name', title = None, header=alt.Header(labelAngle=0)),
        # row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0)),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).properties( 
            height = 100,
            width = 300)

    tti_chart = alt.Chart(df_tti).mark_bar(orient='horizontal').encode(
        y=alt.Y('year', title=None),
        x=alt.X('value', title=None),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        column=alt.Column('Series Name', title = None, header=alt.Header(labelAngle=0)),
        # row=alt.Row('Series Name', title=None, header=alt.Header(labelAngle=0, titleOrient='top')),
        tooltip=['Country Name', 'year', 'value'],
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2))
    ).properties( 
            height = 100,
            width = 300)
    
    chart = (tte_chart & tti_chart).add_selection(click).configure(background='darkkhaki')
    return chart


def create_logistics_performance_chart(df, max, min):
    """
    Create a Plotly radar chart for Logistics Performance Index by country and year and value.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', and 'value'.

    Returns:
        plotly.graph: A plotly radar chart showing Logistics Performance Index by country and year and value.
    """
    countries = df['Country Name'].unique()
    years = df['year'].unique()
    
    fig = go.Figure()
    # tracing layout
    for i in countries:
        fig.add_trace(go.Scatterpolar(
        r=df[(df["Country Name"]==i) &
             df["year"].isin(years)]["value"].values.tolist(),
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
                range=[min, max],
                gridcolor='Black',
            )
        ),
        showlegend=False,
        width=450, 
        height=350, 
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='darkkhaki'
    )

    return fig



