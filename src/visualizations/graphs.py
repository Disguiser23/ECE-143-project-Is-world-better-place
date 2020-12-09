import matplotlib.pyplot as plt
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../')
import pandas as pd
import matplotlib.pylab as pylab



colors_pastel = ['#F8B195', '#F67280', '#C06C84', '#6C5B7B', '#355C7D', '#000000', '#B5EAD7', '#619196', '#FBBA18']


def average_countries_to_continents(dataframe):
    '''this method transforms the values from the specific countries into an average for the continent
    pandas dataframe with countries as index, columns are years
    :param dataframe: pandas.dataframe
    returns: pandas dataframe with continents as index'''
    assert(isinstance(dataframe, pd.DataFrame))
    countries_continents = pd.read_csv('./data/countries_continents/Countries-Continents.csv', index_col=1)
    countries_continents_index =  list(map(lambda x: x.lower(), list(countries_continents.index)))
    countries_continents.index = countries_continents_index
    dataframe_idx = list(map(lambda x: x.lower(), list(dataframe.index)))
    dataframe.index = dataframe_idx
    res = dataframe.join(countries_continents)
    res = res.groupby('Continent').mean()
    return res



def plot_prediction_line_graph(data, pred_df, xlabel, ylabel, title, filename=None):
    '''saves figure as line graph in presentation_images folder
    :param xlabel, ylabel: str axis labels
    :param filename: str or optional
    '''
    assert(isinstance(xlabel, str) and isinstance(ylabel, str) and isinstance(title, str))
    
    params = {'legend.fontsize': 'x-large',
              'figure.figsize': (15, 5),
             'axes.labelsize': 'x-large',
             'axes.titlesize':'x-large',
             'xtick.labelsize':'x-large',
             'ytick.labelsize':'x-large'}
    pylab.rcParams.update(params)
    
    #set up the plot
    ax = data.plot(label='Observed', color=colors_pastel)
    pred_df.plot(ax = ax, label='Forecast', alpha=.7, figsize=(14, 7), color=colors_pastel, legend=False, linestyle='--')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title, fontsize=20)
    if filename:
        plt.savefig('./output_images/'+filename, bbox_inches='tight', transparent=True)
    plt.show()


def stacked_bar_graph_prediction(data, filename=None, title='title', ylabel="Amount"):
    '''plots a stacked bar graph for a dataframe including predictions and saves to presentation_images folder
    :param data: pandas.dataframe
    :param filename: str
    :param title: str or none
    :param ylabel: str'''
    assert(isinstance(data, pd.DataFrame))
    assert(isinstance(title, str))
    assert isinstance(filename, str) or filename == None
    assert (isinstance(ylabel, str))
    params = {'legend.fontsize': 'x-large',
                  'figure.figsize': (15, 5),
                 'axes.labelsize': 'x-large',
                 'axes.titlesize':'x-large',
                 'xtick.labelsize':'x-large',
                 'ytick.labelsize':'x-large'}
    pylab.rcParams.update(params)
    ax =  data.plot(kind='bar', stacked=True, color=colors_pastel, rot=70, title=title)
    ax.set_ylabel(ylabel)
    if filename:
        plt.savefig('./output_images/'+filename, bbox_inches='tight', transparent=True)
    plt.show()