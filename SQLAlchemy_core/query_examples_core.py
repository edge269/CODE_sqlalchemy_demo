import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, ForeignKey, select, and_, distinct, func
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Use in-memory SQLite for demonstration
engine = create_engine('sqlite:///:memory:')
metadata = MetaData()

# Define tables (schema matches the normalized SQL)
reactor_locations = Table(
    "REACTOR_LOCATIONS", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reactor_location", String(32), nullable=False)
)
epochs = Table(
    "EPOCHS", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("epoch", String(8), nullable=False)
)
reactor_design = Table(
    "REACTOR_DESIGN", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reactor_power", Integer, nullable=False),
    Column("reactor_type", String(4), nullable=False)
)
plants = Table(
    "PLANTS", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("plant_name", String(32), nullable=False),
    Column("reactor_location_id", Integer, ForeignKey("REACTOR_LOCATIONS.id"), nullable=False)
)
fuel_assembly = Table(
    "FUEL_ASSEMBLY", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("FA_name", String(8), nullable=False),
    Column("FA_mass", Float, nullable=False),
    Column("FA_length_ft", Integer, nullable=False),
    Column("FA_manufacturing_year", Integer, nullable=False),
    Column("FA_BUp", Float, nullable=False),
    Column("reactor_design_id", Integer, ForeignKey("REACTOR_DESIGN.id"), nullable=False),
    Column("plant_id", Integer, ForeignKey("PLANTS.id"), nullable=False),
    Column("epoch_id", Integer, ForeignKey("EPOCHS.id"), nullable=False),
    Column("introduction_year", Integer, nullable=False)
)

metadata.create_all(engine)

# ---
# IMPORTANT: The denormalized CSV must be parsed and transformed to conform to the normalized database schema.
# This step simulates the normalization process: extracting unique values for lookup tables and mapping them to foreign keys.
# In real-world scenarios, this is a crucial ETL (Extract, Transform, Load) step before populating a normalized database.
print("[INFO] Parsing and normalizing denormalized CSV data to fit the normalized SQL schema...")
# ---
# Use pathlib to construct the path to the data file relative to this script
DATA_PATH = Path(__file__).parent.parent / 'data' / 'plants_data.csv'

# For demo, load the denormalized CSV and simulate normalized inserts
# (In a real case, you would have normalized data and proper FKs)
df = pd.read_csv(DATA_PATH)

# ---
# PEDAGOGICAL NOTE: The following normalization step is designed to explicitly map the denormalized CSV columns to the normalized SQL schema fields, in accordance with the business/domain rules in data/domain_rules.txt.
# This mapping is intentionally verbose to illustrate the normalization process and the importance of data integrity, type safety, and referential consistency.
# Column mapping (CSV → Normalized Schema):
#   reactor_location (CSV) → region (domain rules)
#   reactor_site (CSV)     → plant (domain rules)
#   reactor_power (CSV)    → reactor_power (domain rules)
#   reactor_type (CSV)     → reactor_type (domain rules)
#   reactor_epoch (CSV)    → epoch (domain rules)
#   FA_BUp (CSV)           → FA_BUp (domain rules)
#   FA_mass (CSV)          → FA_mass (domain rules)
#   FA_length_ft (CSV)     → FA_length_ft (domain rules)
#   FA_manufacturing_year (CSV) → FA_manufacturing_year (domain rules)
#   FA_introduction_year (CSV)  → FA_introduction_year (domain rules)
# All fields must be present and non-null. No duplicate FA_name values are allowed.
# If needed, epoch could be recalculated from FA_introduction_year as per the rules, but here we use the CSV value for demonstration.
# ---
# Build lookup tables for normalization (column names adapted to plants_data.csv)
loc_map = {loc: i+1 for i, loc in enumerate(df['region'].unique())}
epoch_map = {ep: i+1 for i, ep in enumerate(df['epoch_label'].unique())}
design_map = {(row['reactor_power_MWe'], row['reactor_type_code']): i+1 for i, row in df.drop_duplicates(['reactor_power_MWe','reactor_type_code']).iterrows()}
plant_map = {(row['plant_code'], row['region']): i+1 for i, row in df.drop_duplicates(['plant_code','region']).iterrows()}

# Insert into lookup tables
with engine.begin() as conn:
    for loc, loc_id in loc_map.items():
        conn.execute(reactor_locations.insert().values(id=loc_id, reactor_location=loc))
    for ep, ep_id in epoch_map.items():
        conn.execute(epochs.insert().values(id=ep_id, epoch=ep))
    for (power, typ), did in design_map.items():
        conn.execute(reactor_design.insert().values(id=did, reactor_power=power, reactor_type=typ))
    for (pname, region), pid in plant_map.items():
        conn.execute(plants.insert().values(id=pid, plant_name=pname, reactor_location_id=loc_map[region]))
    # Insert FUEL_ASSEMBLY
    for _, row in df.iterrows():
        conn.execute(fuel_assembly.insert().values(
            FA_name=row['FA_name'],
            FA_mass=row['FA_mass_kg'],
            FA_length_ft=row['FA_length_ft'],
            FA_manufacturing_year=row['FA_year_made'],
            FA_BUp=row['burnup_GWd_tU'],
            reactor_design_id=design_map[(row['reactor_power_MWe'], row['reactor_type_code'])],
            plant_id=plant_map[(row['plant_code'], row['region'])],
            epoch_id=epoch_map[row['epoch_label']],
            introduction_year=row['FA_year_intro']
        ))

# ---
# Query 1: List all fuel assembly names (FA_name) used in 900 MWe reactors.
# Query 2: Retrieve the burnup (FA_BUp) of fuel assemblies in the Auvergne-Rhône-Alpes region and of CPY reactor design.
# Query 3: Find the maximum and minimum burnup (FA_BUp) for the assemblies selected in Query 2.
# Query 4: Count the number of fuel assemblies in the VD3 epoch and 1450 MWe reactors.
# Query 5: List distinct plant names and their regions for 1300 MWe plants located in the northernmost regions of France.
# ---
# Now run the queries from sqlite3/query_examples.sql
with engine.connect() as conn:
    print("\nQuery 1: FA_name in 900 MWe reactors")
    q1 = select(fuel_assembly.c.FA_name).join(reactor_design, fuel_assembly.c.reactor_design_id == reactor_design.c.id).where(reactor_design.c.reactor_power == 900)
    print(pd.read_sql(q1, conn).head())

    print("\nQuery 2: BUp in Auvergne-Rhône-Alpes and CPY design")
    q2 = select(fuel_assembly.c.FA_BUp).join(reactor_design, fuel_assembly.c.reactor_design_id == reactor_design.c.id)
    q2 = q2.join(plants, fuel_assembly.c.plant_id == plants.c.id)
    q2 = q2.join(reactor_locations, plants.c.reactor_location_id == reactor_locations.c.id)
    q2 = q2.where(and_(reactor_locations.c.reactor_location == 'Auvergne-Rhône-Alpes', reactor_design.c.reactor_type == 'CPY'))
    print(pd.read_sql(q2, conn).head())

    print("\nQuery 3: Max/Min BUp for Query 2")
    q3 = select(
        func.max(fuel_assembly.c.FA_BUp).label('max_bup'),
        func.min(fuel_assembly.c.FA_BUp).label('min_bup')
    ).join(reactor_design, fuel_assembly.c.reactor_design_id == reactor_design.c.id)
    q3 = q3.join(plants, fuel_assembly.c.plant_id == plants.c.id)
    q3 = q3.join(reactor_locations, plants.c.reactor_location_id == reactor_locations.c.id)
    q3 = q3.where(and_(reactor_locations.c.reactor_location == 'Auvergne-Rhône-Alpes', reactor_design.c.reactor_type == 'CPY'))
    print(pd.read_sql(q3, conn))

    print("\nQuery 4: Number of FA in VD3 and 1450 MWe")
    q4 = select(fuel_assembly.c.id).join(reactor_design, fuel_assembly.c.reactor_design_id == reactor_design.c.id)
    q4 = q4.join(epochs, fuel_assembly.c.epoch_id == epochs.c.id)
    q4 = q4.where(and_(epochs.c.epoch == 'VD3', reactor_design.c.reactor_power == 1450))
    print(pd.read_sql(q4, conn).shape[0])

    print("\nQuery 5: 1300 MWe plants in northernmost regions")
    northern_regions = ['Hauts-de-France', 'Île-de-France', 'Normandy', 'Grand Est']
    q5 = select(distinct(plants.c.plant_name), reactor_locations.c.reactor_location)
    q5 = q5.select_from(fuel_assembly.join(plants, fuel_assembly.c.plant_id == plants.c.id)
        .join(reactor_locations, plants.c.reactor_location_id == reactor_locations.c.id)
        .join(reactor_design, fuel_assembly.c.reactor_design_id == reactor_design.c.id))
    q5 = q5.where(and_(reactor_design.c.reactor_power == 1300, reactor_locations.c.reactor_location.in_(northern_regions)))
    print(pd.read_sql(q5, conn).head())

# Create a session for SQLite
script_dir = Path(__file__).resolve().parent
core_db_path = script_dir / 'example_core.db'
sqlite_engine = create_engine(f'sqlite:///{core_db_path}')
metadata.create_all(sqlite_engine)  # create tables in example_core.db
SessionSQLite = sessionmaker(bind=sqlite_engine)
session_sqlite = SessionSQLite()

# Example query for SQLite
print("-- SQLite Query Example --")
result_sqlite = session_sqlite.query(fuel_assembly).filter(fuel_assembly.c.FA_mass > 500).all()
for row in result_sqlite:
    print(row)

# Create a session for Oracle
# Oracle example (wrapped in try/except to avoid invalid connection errors)
try:
    oracle_engine = create_engine('oracle://user:password@host:port/service_name')
    SessionOracle = sessionmaker(bind=oracle_engine)
    session_oracle = SessionOracle()

    # Example query for Oracle
    print("-- Oracle Query Example --")
    result_oracle = session_oracle.query(fuel_assembly).filter(fuel_assembly.c.FA_mass > 500).all()
    for row in result_oracle:
        print(row)
except Exception as e:
    print(f"[INFO] Skipping Oracle example: {e}")
