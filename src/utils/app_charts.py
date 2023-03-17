import altair as alt

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
        width=300,
        height=250,
        title={"text": "Cost to implement business", "fontSize": 14, "fontWeight": "bold", "anchor": "middle"}
    )

    time_chart = (alt.Chart(df_tts).mark_line(point=True).encode(
        alt.X('year:T', scale=alt.Scale(zero=False), title=None),
        alt.Y('value:Q', title="Time required to start a business (days)"),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        tooltip=['Country Name', 'year', 'value']
    ).properties(
        width=300,
        height=250,
        title={"text": "Time to implement business", "fontSize": 14, "fontWeight": "bold", "anchor": "middle"}
    ))

    chart = (cost_chart | time_chart).add_selection(click)

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
        fill='palegreen',
        stroke='white'
    ).project(
        "equirectangular"
    ).properties(
        width=800,
        height=250
    )

    points = alt.Chart(mergedf).mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.value(35),
        color='Country Name:N',
        tooltip='Country Name'
    )

    chart = (background + points).configure_legend(title=None)
    return chart


def create_interest_rate_chart(df):
    """
    Create an Altair line chart for interest rate spread by country and year.

    Args:
        df (pd.DataFrame): A data frame containing columns 'year', 'value', and 'Country Name'.

    Returns:
        alt.Chart: An Altair line chart showing interest rate spread by country and year.
    """
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('year:T', scale=alt.Scale(zero=False), title=None),
        y=alt.Y('value:Q', title="Interest Rate Spread", axis=alt.Axis(labelFontSize=12, titleFontSize=14)),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        tooltip=['Country Name', 'year', 'value']
    ).properties(
        height=200,
        width=700
    )
    return chart


def create_unemployment_rate_chart(df):
    """
    Create an Altair bar chart for unemployment rate by country, year, and education level.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', 'value', and 'education_level'.

    Returns:
        alt.Chart: An Altair bar chart showing unemployment rate by country, year, and education level.
    """
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('education_level:N', title=None, axis=alt.Axis(labels=False, ticks=False)),
        y=alt.Y('value:Q', title="Unemployment Rate", axis=alt.Axis(titleFontSize=14)),
        color=alt.Color('education_level:N', legend=alt.Legend(title='Education Level', orient='bottom', columns=len(df['education_level'].unique()))),
        column=alt.Column('Country Name:N', title=None),
        tooltip=['Country Name', 'year', 'value']
    ).properties(
        height=250,
        width=100
    ).configure_view(
        stroke='transparent'
    )

    return chart


def create_participation_rate_chart(df):
    """
    Create an Altair bar chart for participation rate by country and year.

    Args:
        df (pd.DataFrame): A data frame containing columns 'Country Name', 'year', and 'value'.

    Returns:
        alt.Chart: An Altair bar chart showing participation rate by country and year.
    """
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('value:Q', title="Participation Rate", axis=alt.Axis(titleFontSize=14)),
        y=alt.Y('Country Name:N', title=None),
        color=alt.Color('Country Name', legend=alt.Legend(title=None)),
        tooltip=['Country Name', 'year', 'value']
    ).properties(
        height=300,
        width=300
    )

    return chart

