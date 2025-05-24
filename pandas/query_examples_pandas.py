import pandas as pd
from pathlib import Path

# Use pathlib to construct the path to the data file relative to this script
DATA_PATH = Path(__file__).parent.parent / 'data' / 'plants_data.csv'

# Load the pedagogical CSV file (denormalized, flat structure)
df = pd.read_csv(DATA_PATH)

# Query 1: Get the name of all Fuel Assemblies in 900 MWe reactors
fa_900 = df[df['reactor_power_MWe'] == 900]['FA_name']
print('Query 1: FA_name in 900 MWe reactors')
print(fa_900.head(), '\n')

# Query 2: Get the BUp of all Fuel Assemblies implemented in the Auvergne-Rhône-Alpes region and that are in the CPY design
bup_cpy_auvergne = df[(df['region'] == 'Auvergne-Rhône-Alpes') & (df['reactor_type_code'] == 'CPY')]['burnup_GWd_tU']
print('Query 2: BUp in Auvergne-Rhône-Alpes and CPY design')
print(bup_cpy_auvergne.head(), '\n')

# Query 3: Get the max and min Burnup for the above selection
if not bup_cpy_auvergne.empty:
    print('Query 3: Max/Min BUp for Query 2')
    print('Max:', bup_cpy_auvergne.max(), 'Min:', bup_cpy_auvergne.min(), '\n')
else:
    print('Query 3: No data for Query 2 selection\n')

# Query 4: Number of Fuel Assemblies that are in VD3 epoch and on 1450 MWe core designs
count_vd3_1450 = df[(df['epoch_label'] == 'VD3') & (df['reactor_power_MWe'] == 1450)].shape[0]
print('Query 4: Number of FA in VD3 and 1450 MWe:', count_vd3_1450, '\n')

# Query 5: List all 1300 MWe Plants in the Northernmost French Regions
northern_regions = ['Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est']
plants_1300 = df[(df['reactor_power_MWe'] == 1300) & (df['region'].isin(northern_regions))][['plant_name', 'region']].drop_duplicates()
print('Query 5: 1300 MWe plants in northernmost regions')
print(plants_1300.head(), '\n')

# Pedagogical note: These queries are much more verbose and error-prone in pandas due to the flat, denormalized structure of the CSV, compared to normalized SQL joins.
