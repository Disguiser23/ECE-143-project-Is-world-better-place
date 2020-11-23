# requires conda install basemap
# adapted to generalize from https://python-graph-gallery.com/315-a-world-map-of-surf-tweets/
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def create_world_bubble_map(data, label, filename, ):
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

    coords = pd.DataFrame([[-55.59, -10, 'South America'], [-3.69, 51.53, 'Europe'],
        [25, 6.77, 'Africa'], [79.57, 44.52, 'Asia'], [125.69, -25.45, 'Oceania'],
        [-100.04, 42.51, 'North America']])
    coords.columns = ['lon', 'lat', 'Continent']
    coords = coords.set_index('Continent')
    data = data.join(coords)
    data['labels_enc'] = pd.factorize(data.index)[0]
    df = data['data']
    m.scatter(data['lon'], data['lat'], s=df, c=data['labels_enc'], cmap="Set1")
    plt.text(-170, -58, label,
         ha='left', va='bottom', size=30, color='#555555')

    plt.savefig(filename, bbox_inches='tight')

if __name__ =="__main__":
    csv = pd.read_csv('./visualizations/test/avg_gdp_continents.csv', index_col=0)
    data = pd.DataFrame(csv['1970']/ 1000000)
    data = data.rename(columns={"1970": "data"})
    create_world_bubble_map(data, "label", 'test.png')
