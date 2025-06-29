# SQLAlchemy Core Summary

## Overview

The creation of tables and execution of queries using SQLAlchemy Core are now strictly identical for both SQLite and Oracle. The only difference lies in the session binding, which determines the database engine being used.

## Imports

The following imports are used in the script:

```python
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import sqlite, oracle
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
```

## Example: `FUEL_ASSEMBLY` Table Definition

Below is the SQLAlchemy Core definition for the `FUEL_ASSEMBLY` table:

```python
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
```

## Example Queries

### SQLite Session

```python
sqlite_engine = create_engine('sqlite:///example.db')
SessionSQLite = sessionmaker(bind=sqlite_engine)
session_sqlite = SessionSQLite()

result_sqlite = session_sqlite.query(fuel_assembly).filter(fuel_assembly.c.FA_mass > 500).all()
for row in result_sqlite:
    print(row)
```

### Oracle Session

```python
oracle_engine = create_engine('oracle://user:password@host:port/service_name')
SessionOracle = sessionmaker(bind=oracle_engine)
session_oracle = SessionOracle()

result_oracle = session_oracle.query(fuel_assembly).filter(fuel_assembly.c.FA_mass > 500).all()
for row in result_oracle:
    print(row)
```

## Key Takeaway

By using SQLAlchemy Core, the table definitions and queries remain consistent across different database engines. The only adjustment required is the session binding to the appropriate engine.
