# ECE143 Project: Is the world going to be a better place? (Team 23)
This project was motivated by the fact that during the 2020 global pandemic, we all needed some encouragement. We wanted to analyze if the world is actually improving, even though we are constantly exposed to more bad than good  news.
## Used Libraries
Pandas (Version 1.1.4)

Matplotlib (Version 3.1.1),
mpl_toolkits.basemap (requires conda install basemap)

statsmodels.api (Version 0.10.1)

## Datasets
* Health
    * Gender equality [[8](http://data.un.org/DocumentData.aspx?id=415)], 
                    [[7](https://databank.worldbank.org/source/gender-statistics)],
                    [[11](http://hdr.undp.org/en/data#)]
    * Death rates by causes [[1](http://data.un.org/Data.aspx?d=POP&f=tableCode%3a105)], 
                    [[2](https://ourworldindata.org/ofdacred-international-disaster-data)]
    * Happiness and Life Satisfaction [[9](https://www.kaggle.com/unsdsn/world-happiness)]
* Economy
    * Employment rates [[3](https://stats.oecd.org/index.aspx?queryid=36324#)], 
                    [[12](http://hdr.undp.org/en/data#)]
    * GDP [[4](http://data.un.org/Data.aspx?d=SNAAMA&f=grID%3a101%3bcurrID%3aUSD%3bpcFlag%3a0%3bitID%3a9)]
* Environmental  
    * Disasters [[6](https://earthdata.nasa.gov/earth-observation-data/near-real-time/hazards-and-disasters/drought)] 
    [[5](https://www.emdat.be/)]
    * Greenhouse Gas Emissions [[10](https://github.com/owid/co2-data)]

## File Structure
```bash
.
├── README.md
├── data
│   ├── countries_continent
│   ├── economy      
│   ├── environmental   
│   └── health      
├── src                    
│   ├── data_loading  
│       ├── clean_health_data.py          
│       ├── clean_economy_data.py       
│       └── clean_disaster_data.py
│   ├── predictions
│       ├── predictions.py       
│       └── world_overall.py 
│   └── visualizations     
│       ├── envi_merge.py
│       ├── graphs.py       
│       ├── read_co2.py     
│       ├── read_disaster.py         
│       └── world_map.py
├── main.ipynb
├── health.py
├── economy.py
├── environment.py
├── output_images
├── .gitignore
└── ECE_143_Is_world_better_place.pdf
```
## How to run the code
Directly run main.ipynb

## Final Presentation
Can be found in ./final_presentation/ECE_143_Is_world_better_place.pdf



