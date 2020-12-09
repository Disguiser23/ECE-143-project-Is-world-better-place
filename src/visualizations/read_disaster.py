import pandas as pd
import numpy as np
import plotly.express as px
import os

curr_path = os.path.split(os.path.realpath(__file__))[0]
curr_path = os.path.dirname(curr_path)
curr_path = os.path.dirname(curr_path)
curr_path += '\\data\\environmental\\'

def read_total_natural_disaster():
    '''
    This function read number-of-natural-disaster.cvs and return a Dataframe
    contains the total number of natual disaster
    :returns: pd.Dataframe
    '''

    origin_data = pd.read_csv(curr_path + 'number-of-natural-disaster-events.csv')
    origin_data = origin_data.drop(
        origin_data[~origin_data['Entity'].str.contains('All natural disasters'
                                                        )].index)
    origin_data = origin_data.drop(labels='Entity', axis=1)
    origin_data.reset_index(drop=True, inplace=True)
    return origin_data


def fig_total_natural_disaster():
    '''
    This function used the dataframe returned by read_total_natural_disaster
    and generateds a ploty fig object
    :returns: plotly.graph_objs._figure.Figure
    '''

    df = read_total_natural_disaster()
    fig = px.line(df,
                  x="Year",
                  y="Number of disasters (EMDAT (2020))",
                  line_shape="spline",
                  render_mode="svg")
    fig.update_layout(title='Total Number of Natural Disasters')
    return fig


def read_natural_disaster():
    '''
    This function read number-of-natural-disaster.cvs and return a Dataframe
    contains the number of different types of natual disaster
    :returns: pd.Dataframe
    '''

    origin_data = pd.read_csv(curr_path + 'number-of-natural-disaster-events.csv')
    origin_data = origin_data.drop(origin_data[
        origin_data['Entity'].str.contains('All natural disasters')].index)
    origin_data.rename(columns={"Entity": "Type"}, inplace=True)
    origin_data.reset_index(drop=True, inplace=True)
    return origin_data


def fig_natural_disaster():
    '''
    This function used the dataframe returned by read_total_natural_disaster
    and generateds a ploty fig object
    :returns: plotly.graph_objs._figure.Figure
    '''

    df = read_natural_disaster()
    fig = px.line(df,
                  x="Year",
                  y="Number of disasters (EMDAT (2020))",
                  color='Type',
                  hover_name="Type",
                  line_shape="spline",
                  render_mode="svg")
    fig.update_layout(title='Number of Natural Disasters')
    return fig

#read_total_natural_disaster()