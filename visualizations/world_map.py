# requires conda install basemap
# adapted to generalize from https://python-graph-gallery.com/315-a-world-map-of-surf-tweets/
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import colors_red_to_green


def create_world_bubble_map(data, label, filename):
    '''input: data is a pandas dataframe with a column 'data' and 'Continent
    label is the label to be displayed
    filename must include file suffix
    countries'''
    my_dpi = 96
    plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi)
    # Make the background map
    m = Basemap(llcrnrlon=-180, llcrnrlat=-65, urcrnrlon=180, urcrnrlat=80)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.3)
    m.drawcoastlines(linewidth=0.1, color="white")

    coords = pd.DataFrame([[-55.59, -10, 'South America', 'Health'],[-55.59, -10, 'South America', 'Environment'],[-55.59, -10, 'South America', 'Economy'],
                           [-3.69, 51.53, 'Europe', 'Health'], [-3.69, 51.53, 'Europe', 'Environment'], [-3.69, 51.53, 'Economy'],
                           [25, 6.77, 'Africa', 'Health'], [25, 6.77, 'Africa', 'Environment'], [25, 6.77, 'Africa', 'Economy'],
                           [79.57, 44.52, 'Asia', 'Health'], [79.57, 44.52, 'Asia', 'Environment'], [79.57, 44.52, 'Asia', 'Economy'],
                           [125.69, -25.45, 'Oceania', 'Health'], [125.69, -25.45, 'Oceania', 'Environment'], [125.69, -25.45, 'Oceania', 'Economy'],
                           [-100.04, 42.51, 'North America', 'Health'], [-100.04, 42.51, 'North America', 'Environment'], [-100.04, 42.51, 'North America', 'Economy']])
    coords.columns = ['lon', 'lat', 'Continent', 'Category']
    coords = coords.set_index('Continent')
    data = data.join(coords)
    data['labels_enc'] = pd.factorize(data.index)[0]
    print(pd.factorize(data.index)[0])
    df = data['data']
    m.scatter(data['lon'], data['lat'], s=df, c=data['labels_enc'], color=colors_red_to_green)
    plt.text(-170, -58, label,
         ha='left', va='bottom', size=30, color='#555555')

    plt.savefig(filename, bbox_inches='tight')

if __name__ =="__main__":
    csv = pd.read_csv('./visualizations/avg_gdp_continents.csv', index_col=0)
    data = pd.DataFrame(csv['1970']/ 1000000)
    data = data.rename(columns={"1970": "data"})
    create_world_bubble_map(data, "label", 'test.png')
