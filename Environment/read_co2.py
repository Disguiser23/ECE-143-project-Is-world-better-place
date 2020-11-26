import pandas as pd
import numpy as np
import plotly.express as px
import os, sys
sys.path.append('../')
from predictions.predictions import autoregressive_integrated_moving_average
from visualizations.graphs import plot_prediction_line_graph, stacked_bar_graph_prediction
from utils import colors_pastel

def read_co2_continent(year_start=1900, year_end=2018):
    '''
    This function reads the amounts of CO2 emission of the world and each
    continents from 1900 to 2018. The data was rearranged.
    :param year_start: The start year
    :type year_start: int
    :param year_end: The end year
    :type year_end: int
    :returns: pd.Dataframe
    '''
    assert isinstance(year_start, int)
    assert isinstance(year_end, int)
    assert 1900 <= year_start < year_end
    assert year_end <= 2018

    origin_data = pd.read_csv('./data/owid-co2-data.csv', usecols=[1, 2, 3])
    continents = [
        'World', 'Africa', 'Asia', 'Europe', 'Oceania', 'North America',
        'South America'
    ]

    origin_data = origin_data.drop(
        origin_data[origin_data['year'] < year_start].index)
    origin_data = origin_data.drop(
        origin_data[~origin_data['country'].isin(continents)].index)

    origin_data.rename(columns={"country": "area"}, inplace=True)
    origin_data.reset_index(drop=True, inplace=True)
    return origin_data


def fig_co2_continent():
    '''
    This function used the dataframe returned by read_co2_continent
    and generateds a ploty fig object
    :returns: plotly.graph_objs._figure.Figure
    '''

    df = read_co2_continent()
    fig = px.line(df,
                  x="year",
                  y="co2",
                  color='area',
                  line_shape="spline",
                  render_mode="svg")
    fig.update_layout(
        title='The amount of CO<sub>2</sub> Emission of Each Continent',
        xaxis_title='Year',
        yaxis_title='Annual CO<sub>2</sub> Emission, Million Tonnes per Year')
    return fig


def read_co2_trans():
    '''
    This function reads the amounts of CO2 emission of international.
    The data was rearranged with year as index
    :returns: pd.Dataframe
    '''
    origin_data = pd.read_csv('./data/owid-co2-data.csv', usecols=[1, 2, 3])
    origin_data = origin_data.drop(
        origin_data[~origin_data['country'].str.
                    contains('International transport')].index)
    origin_data = origin_data.drop(origin_data[origin_data['co2'] == 0].index)
    origin_data = origin_data.drop(labels='country', axis=1)
    origin_data.reset_index(drop=True, inplace=True)

    return origin_data


def fig_co2_trans():
    '''
    This function used the dataframe returned by read_co2_continent
    and generateds a ploty fig object
    :returns: plotly.graph_objs._figure.Figure
    '''

    df = read_co2_trans()
    fig = px.line(df,
                  x="year",
                  y="co2",
                  line_shape="spline",
                  render_mode="svg")
    fig.update_layout(
        title=
        'The amount of CO<sub>2</sub> Emission of Internatioanl Transportation',
        xaxis_title='Year',
        yaxis_title='Annual CO<sub>2</sub> Emission, Million Tonnes per Year')
    return fig


def get_country_continent_dict():
    '''
    This function read country-and-continent-codes-list.csv and generate a
    dictionary with iso country code as keys and corresponding continents as
    values.
    :returns: dict
    '''
    df = pd.read_csv('./data/country-and-continent-codes-list.csv',
                     usecols=[0, 4])
    df.drop(df[df['Three_Letter_Country_Code'].isna()].index, inplace=True)
    df.drop_duplicates(subset='Three_Letter_Country_Code',
                       keep='first',
                       inplace=True)
    dict_df = df.set_index('Three_Letter_Country_Code').T.to_dict('list')
    for key in dict_df.keys():
        dict_df[key] = dict_df[key][0]
    return dict_df


def read_co2_country(year_start=1990, year_end=2018):
    '''
    This function reads the amounts of CO2 emission of each country.
    The data was rearranged and added corresponding continent
    :param year_start: The start year
    :type year_start: int
    :param year_end: The end year
    :type year_end: int
    :returns: pd.Dataframe
    '''

    assert isinstance(year_start, int)
    assert isinstance(year_end, int)
    assert 1900 <= year_start <= year_end
    assert year_end <= 2018

    origin_data = pd.read_csv('./data/owid-co2-data.csv', usecols=[0, 1, 2, 3])
    origin_data = origin_data.drop(
        origin_data[origin_data['year'] < year_start].index)
    origin_data = origin_data.drop(
        origin_data[origin_data['year'] > year_end].index)
    origin_data = origin_data.drop(origin_data[origin_data['iso_code'].isin(
        [np.nan, 'OWID_WRL', 'OWID_KOS'])].index)
    origin_data.set_index('iso_code', inplace=True)

    dict_cont = get_country_continent_dict()
    origin_data['continent'] = pd.Series(dict_cont)
    origin_data.reset_index(inplace=True)
    return origin_data


def fig_sunburst_co2_country(curr_year=2018):
    '''
    This function used the dataframe returned by read_co2_country
    and generateds a plotly fig object. It will generate a sunburst figure
    illustrating the CO2 emmision of different countries in a certain year
    :param curr_year: The year that concerned
    :type cyrr_year: int
    :returns: plotly.graph_objs._figure.Figure
    '''
    df = read_co2_country(curr_year, curr_year)
    fig = px.sunburst(df.query('year == @curr_year'),
                      path=['continent', 'country'],
                      values='co2',
                      color='co2',
                      hover_data=['iso_code'])
    fig.update_layout(
        title='The amount of CO<sub>2</sub> Emission of Each Country in {}'.
        format(curr_year),
        coloraxis_colorbar_title='Annual CO<sub>2</sub>')
    return fig


def fig_map_co2_country(year_start=1990, year_end=2018):
    '''
    This function used the dataframe returned by read_co2_country
    and generateds a plotly fig object. It will generate a world map plot
    uisng color to illustrate the amount of CO2 generated by different country.
    The figure use the year as frame.
    :param year_start: year of starting plotting
    :type year_start: int
    :param year_end: year of ending plotting
    :type year_end: int
    :returns: plotly.graph_objs._figure.Figure
    '''
    df = read_co2_country(year_start, year_end)
    fig = px.choropleth(df,
                        locations="iso_code",
                        color="co2",
                        hover_name="country",
                        animation_frame="year",
                        range_color=[0, 10000])

    fig.update_layout(
        title='The Amount of CO<sub>2</sub> Emission of Each Country',
        coloraxis_colorbar_title='Annual CO<sub>2</sub>')

    return fig


def get_predict_co2_continent(year_start = 1900, year_end = 2018):
    '''
    This function call autoregressive_integrated_moving_average to predict
    the co2 emission of each continent
    '''
    df_origin = read_co2_continent(year_start, year_end)
    area = [
        'World', 'Africa', 'Asia', 'Europe', 'Oceania', 'North America',
        'South America'
    ]
    years = list(range(year_start, year_end + 1))
    temp = np.zeros([len(years), len(area)])
    df_new = pd.DataFrame(temp, columns=area, index=years, dtype=float)

    for _, row in df_origin.iterrows():
        df_new[row['area']][row['year']] = row['co2']

    _, df_pre = autoregressive_integrated_moving_average(df_new, steps=20, seasonal_order = None)
    df_pre.drop(labels='Year', axis=1)

    return df_new, df_pre

def plot_predict_co2_continent(year_start = 1900, year_end = 2018, file_name = None):
    '''
    This function call plot_prediction_line_graph to draw the line graph
    '''
    df, df_pre = get_predict_co2_continent(year_start, year_end)
    plot_prediction_line_graph(df, df_pre, 'Year', 'CO${_2}$', 'CO${_2}$ of Each Continent and the World with Prediction', file_name)
