import pandas as pd

def get_selected_countries(data, countries, value_range, series_name):
    """
    Return a list of countries with mean values within the specified range for a given series. 
    These countries will also be used as a chained filter for remaining charts.

    Args:
        data (pd.DataFrame): The input data frame containing country, series name, and value information.
        countries (list): A list of country names to consider for filtering.
        value_range (tuple): A tuple with two values, representing the minimum and maximum values for the specified series.
        series_name (str): The name of the series to consider for filtering.

    Returns:
        list: A list of countries with mean values within the specified range for the given series.
    """
    min_rate = value_range[0]
    max_rate = value_range[1]
    series_name = series_name
    df = data[(data['Country Name'].isin(countries)) & (data['Series Name'] == series_name)]

    mean_rates = df.groupby('Country Name')['value'].mean().reset_index()
    selected_countries = mean_rates[(mean_rates['value'] >= min_rate) & (mean_rates['value'] <= max_rate)]['Country Name']

    return selected_countries


def get_countries_based_on_sliders(df, countries, sliders_series):
    """
    Get selected countries based on different slider values.

    Parameters:
    df (pd.DataFrame): Original dataframe containing the data
    countries (list): List of countries to consider
    sliders_series (list): List of tuples containing slider values and their corresponding series names

    Returns:
    pd.Series: A pandas Series object containing the selected countries
    """
    selected_countries_list = []
    
    for slider_value, series_name in sliders_series:
        if slider_value is not None:
            selected_countries = get_selected_countries(df, countries, slider_value, series_name)
        else:
            selected_countries = countries
        selected_countries_list.append(selected_countries)

    # Get the intersection of all selected countries lists
    selected_countries = pd.Series(list(set(selected_countries_list[0]).intersection(*selected_countries_list[1:])))
    return selected_countries

