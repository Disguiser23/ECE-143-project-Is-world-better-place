import matplotlib.pyplot as plt
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('../')
from utils import colors_pastel
import pandas as pd

def plot_prediction_line_graph(data, pred_df, xlabel, ylabel, title, filename):
    '''xlabel, ylabel: str axis labels
    optional filename: str
    saves figure
    returns None'''
    assert(isinstance(xlabel, str) and isinstance(ylabel, str) and isinstance(filename, str) and isinstance(title, str))

    #set up the plot
    ax = data.plot(label='Observed', color=colors_pastel)
    pred_df.plot(ax = ax, label='Forecast', alpha=.7, figsize=(14, 7), color=colors_pastel, legend=False, linestyle='--')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()


def stacked_bar_graph_prediction(data, filename="stacked_bar_graph.png", title='title', ylabel="Amount"):
    assert(isinstance(data, pd.DataFrame))
    assert(isinstance(filename, str) and isinstance(title, str))

    ax =  data.plot(kind='bar', stacked=True, color=colors_pastel, rot=70, title=title)
    ax.set_ylabel(ylabel)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()