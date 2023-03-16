import altair as alt
import pandas as pd

def get_selected_countries(data, countries, interest_rate_range):
    """
    Return a list of countries with mean interest rates within the specified range. These countries will also be used as chained
    filter for remaining charts in resources tab.

    Args:
        data (pd.DataFrame): The input data frame containing country, series name, and interest rate information.
        countries (list): A list of country names to consider for filtering.
        interest_rate_range (tuple): A tuple with two values, representing the minimum and maximum interest rate.

    Returns:
        list: A list of countries with mean interest rates within the specified range.
    """
    min_rate = interest_rate_range[0]
    max_rate = interest_rate_range[1]
    series_name = 'Interest rate spread (lending rate minus deposit rate, %)'
    df = data[(data['Country Name'].isin(countries)) & (data['Series Name'] == series_name)]

    mean_rates = df.groupby('Country Name')['value'].mean().reset_index()
    selected_countries = mean_rates[(mean_rates['value'] >= min_rate) & (mean_rates['value'] <= max_rate)]['Country Name']

    return selected_countries


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
