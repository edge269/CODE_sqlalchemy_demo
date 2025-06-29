import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_tables_orm import ReactorLocation, Epoch, ReactorDesign, Plant, FuelAssembly
from pathlib import Path
from typing import Dict, Tuple

# Load data from CSV
DATA_PATH = Path(__file__).parent.parent / 'data' / 'plants_data.csv'
df = pd.read_csv(DATA_PATH)

# Create SQLite session
DB_PATH = Path(__file__).parent / 'example_orm.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data in tables
session.query(Epoch).delete()
session.query(ReactorLocation).delete()
session.query(ReactorDesign).delete()
session.query(Plant).delete()
session.query(FuelAssembly).delete()
session.commit()

# Build lookup tables with type annotations
loc_map: Dict[str, int] = {loc: idx + 1 for idx, loc in enumerate(df['region'].astype(str).unique())}
epoch_map: Dict[str, int] = {ep: idx + 1 for idx, ep in enumerate(df['epoch_label'].astype(str).unique())}
design_map: Dict[Tuple[int, str], int] = {
    (int(df.at[idx, 'reactor_power_MWe']), str(df.at[idx, 'reactor_type_code'])): idx + 1
    for idx in df.drop_duplicates(['reactor_power_MWe', 'reactor_type_code']).index
}
plant_map: Dict[Tuple[str, str], int] = {
    (str(df.at[idx, 'plant_code']), str(df.at[idx, 'region'])): idx + 1
    for idx in df.drop_duplicates(['plant_code', 'region']).index
}

# Insert data into tables
for loc, loc_id in loc_map.items():
    session.add(ReactorLocation(id=loc_id, reactor_location=loc))
for ep, ep_id in epoch_map.items():
    session.add(Epoch(id=ep_id, epoch=ep))
for (power, typ), did in design_map.items():
    session.add(ReactorDesign(id=did, reactor_power=power, reactor_type=typ))
for (pname, region), pid in plant_map.items():
    session.add(Plant(id=pid, plant_name=pname, reactor_location_id=loc_map[region]))
for _, row in df.iterrows():
    session.add(FuelAssembly(
        FA_name=row.at['FA_name'],
        FA_mass=row.at['FA_mass_kg'],
        FA_length_ft=row.at['FA_length_ft'],
        FA_manufacturing_year=row.at['FA_year_made'],
        FA_BUp=row.at['burnup_GWd_tU'],
        reactor_design_id=design_map[(int(row.at['reactor_power_MWe']), str(row.at['reactor_type_code']))],
        plant_id=plant_map[(str(row.at['plant_code']), str(row.at['region']))],
        epoch_id=epoch_map[str(row.at['epoch_label'])],
        introduction_year=row.at['FA_year_intro']
    ))

session.commit()
print("Data uploaded successfully.")
