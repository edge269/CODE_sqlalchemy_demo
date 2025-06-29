from sqlalchemy import create_engine, func, and_
from sqlalchemy.orm import sessionmaker
from create_tables_orm import FuelAssembly, ReactorDesign, Plant, ReactorLocation, Epoch
from pathlib import Path

# Create SQLite session
DB_PATH = Path(__file__).parent / 'example_orm.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
Session = sessionmaker(bind=engine)
session = Session()

# Query 1: List all fuel assembly names (FA_name) used in 900 MWe reactors
print("\nQuery 1: FA_name in 900 MWe reactors")
result = session.query(FuelAssembly.FA_name).join(ReactorDesign).filter(ReactorDesign.reactor_power == 900).all()
print(result)

# Query 2: Retrieve the burnup (FA_BUp) of fuel assemblies in the Auvergne-Rhône-Alpes region and of CPY reactor design
print("\nQuery 2: BUp in Auvergne-Rhône-Alpes and CPY design")
result = session.query(FuelAssembly.FA_BUp).join(ReactorDesign).join(Plant).join(ReactorLocation).filter(
    and_(ReactorLocation.reactor_location == 'Auvergne-Rhône-Alpes', ReactorDesign.reactor_type == 'CPY')
).all()
print(result)

# Query 3: Find the maximum and minimum burnup (FA_BUp) for the assemblies selected in Query 2
print("\nQuery 3: Max/Min BUp for Query 2")
result = session.query(
    func.max(FuelAssembly.FA_BUp).label('max_bup'),
    func.min(FuelAssembly.FA_BUp).label('min_bup')
).join(ReactorDesign).join(Plant).join(ReactorLocation).filter(
    and_(ReactorLocation.reactor_location == 'Auvergne-Rhône-Alpes', ReactorDesign.reactor_type == 'CPY')
).all()
print(result)

# Query 4: Count the number of fuel assemblies in the VD3 epoch and 1450 MWe reactors
print("\nQuery 4: Number of FA in VD3 and 1450 MWe")
result = session.query(FuelAssembly).join(ReactorDesign).join(Epoch).filter(
    and_(Epoch.epoch == 'VD3', ReactorDesign.reactor_power == 1450)
).count()
print(result)

# Query 5: List distinct plant names and their regions for 1300 MWe plants located in the northernmost regions of France
print("\nQuery 5: 1300 MWe plants in northernmost regions")
northern_regions = ['Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est']
result = session.query(Plant.plant_name, ReactorLocation.reactor_location).join(ReactorLocation).join(FuelAssembly).join(ReactorDesign).filter(
    and_(ReactorDesign.reactor_power == 1300, ReactorLocation.reactor_location.in_(northern_regions))
).distinct().all()
print(result)
