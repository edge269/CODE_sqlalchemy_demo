from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import sqlite, oracle

metadata = MetaData()

# Define all referenced tables first
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

epochs = Table(
    "EPOCHS", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("epoch", String(8), nullable=False)
)

reactor_locations = Table(
    "REACTOR_LOCATIONS", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reactor_location", String(32), nullable=False)
)

# Now define the FUEL_ASSEMBLY table
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

# Print the CREATE TABLE statements for all tables for SQLite3
print("-- SQLite3 DDL --")
for table in [reactor_locations, epochs, reactor_design, plants, fuel_assembly]:
    print(str(CreateTable(table).compile(dialect=sqlite.dialect())))
    print()

# Print the CREATE TABLE statements for all tables for Oracle
print("\n-- Oracle DDL --")
for table in [reactor_locations, epochs, reactor_design, plants, fuel_assembly]:
    print(str(CreateTable(table).compile(dialect=oracle.dialect())))
    print()
