# SQLAlchemy ORM Table Creation Example

This document provides an example of how SQLAlchemy ORM creates tables in a SQLite database. The focus is on the `FuelAssembly` and `Plant` tables to illustrate the relationships and structure.

## `FuelAssembly` Table

The `FuelAssembly` table represents individual fuel assemblies used in nuclear reactors. Below is the schema:

| Column Name              | Type       | Description                                      |
|--------------------------|------------|--------------------------------------------------|
| `id`                     | Integer    | Primary key, auto-incremented                   |
| `FA_name`                | String(8)  | Name of the fuel assembly                       |
| `FA_mass`                | Float      | Mass of the fuel assembly                       |
| `FA_length_ft`           | Integer    | Length of the fuel assembly in feet             |
| `FA_manufacturing_year`  | Integer    | Year the fuel assembly was manufactured         |
| `FA_BUp`                 | Float      | Burn-up value of the fuel assembly              |
| `reactor_design_id`      | Integer    | Foreign key referencing `ReactorDesign` table   |
| `plant_id`               | Integer    | Foreign key referencing `Plant` table           |
| `epoch_id`               | Integer    | Foreign key referencing `Epoch` table           |
| `introduction_year`      | Integer    | Year the fuel assembly was introduced           |

### Relationships
- **ReactorDesign**: Each fuel assembly is associated with a reactor design.
- **Plant**: Each fuel assembly belongs to a specific plant.
- **Epoch**: Each fuel assembly is linked to a specific epoch.

## `Plant` Table

The `Plant` table represents nuclear plants. Below is the schema:

| Column Name              | Type       | Description                                      |
|--------------------------|------------|--------------------------------------------------|
| `id`                     | Integer    | Primary key, auto-incremented                   |
| `plant_name`             | String(32) | Name of the plant                               |
| `reactor_location_id`    | Integer    | Foreign key referencing `ReactorLocation` table |

### Relationships
- **ReactorLocation**: Each plant is located in a specific reactor location.
- **FuelAssembly**: Each plant can have multiple fuel assemblies.

## Example Code

Below is the code snippet for creating these tables using SQLAlchemy ORM:

```python
class Plant(Base):
    __tablename__ = 'PLANTS'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    plant_name: Mapped[str] = mapped_column(String(32), nullable=False)
    reactor_location_id: Mapped[int] = mapped_column(ForeignKey('REACTOR_LOCATIONS.id'), nullable=False)
    reactor_location: Mapped['ReactorLocation'] = relationship('ReactorLocation', back_populates='plants')
    fuel_assemblies: Mapped[list['FuelAssembly']] = relationship('FuelAssembly', back_populates='plant')

class FuelAssembly(Base):
    __tablename__ = 'FUEL_ASSEMBLY'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    FA_name: Mapped[str] = mapped_column(String(8), nullable=False)
    FA_mass: Mapped[float] = mapped_column(nullable=False)
    FA_length_ft: Mapped[int] = mapped_column(nullable=False)
    FA_manufacturing_year: Mapped[int] = mapped_column(nullable=False)
    FA_BUp: Mapped[float] = mapped_column(nullable=False)
    reactor_design_id: Mapped[int] = mapped_column(ForeignKey('REACTOR_DESIGN.id'), nullable=False)
    plant_id: Mapped[int] = mapped_column(ForeignKey('PLANTS.id'), nullable=False)
    epoch_id: Mapped[int] = mapped_column(ForeignKey('EPOCHS.id'), nullable=False)
    introduction_year: Mapped[int] = mapped_column(nullable=False)
    reactor_design: Mapped['ReactorDesign'] = relationship('ReactorDesign', back_populates='fuel_assemblies')
    plant: Mapped['Plant'] = relationship('Plant', back_populates='fuel_assemblies')
    epoch: Mapped['Epoch'] = relationship('Epoch', back_populates='fuel_assemblies')

# Create SQLite database and tables
DB_PATH = Path(__file__).parent / 'example_orm.db'
engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
engine.dispose()
print("Tables created successfully.")
```

This code snippet demonstrates how SQLAlchemy ORM defines the schema and relationships for the `FuelAssembly` and `Plant` tables. The `create_engine` function is used to connect to the SQLite database, and `Base.metadata.create_all(engine)` creates the tables.

## Upload Script Logic

The upload script (`upload_data_orm.py`) is responsible for inserting data into the tables. It follows these steps:

1. **Clear Existing Data**: Before uploading new data, the script clears all existing data in the tables to avoid unique constraint errors.
2. **Read CSV Data**: The script reads data from the `plants_data.csv` file using `pandas`.
3. **Insert Data**: The script maps the CSV data to ORM objects and inserts them into the database using SQLAlchemy's session management.


### FuelAssembly Upload Example

Below is how each CSV row is transformed into a `FuelAssembly` ORM object using lookup maps for foreign keys:

```python
# after building loc_map, epoch_map, design_map, plant_map
for _, row in df.iterrows():
    assembly = FuelAssembly(
        FA_name=row['FA_name'],
        FA_mass=row['FA_mass_kg'],
        FA_length_ft=row['FA_length_ft'],
        FA_manufacturing_year=row['FA_year_made'],
        FA_BUp=row['burnup_GWd_tU'],
        reactor_design_id=design_map[(int(row['reactor_power_MWe']), row['reactor_type_code'])],
        plant_id=plant_map[(row['plant_code'], row['region'])],
        epoch_id=epoch_map[row['epoch_label']],
        introduction_year=row['FA_year_intro']
    )
    session.add(assembly)
session.commit()
print("Fuel assemblies uploaded successfully.")
```

## Query Example

The query script (`query_data_orm.py`) retrieves data from the database. Below is an example of Query 4:

### Query 4: Count Fuel Assemblies in VD3 Epoch and 1450 MWe Reactors

This query counts the number of fuel assemblies matching specific criteria using SQLAlchemy ORM.

```python
result = session.query(func.count(FuelAssembly.id))\
    .join(ReactorDesign)\
    .join(Epoch)\
    .filter(
        and_(Epoch.epoch == 'VD3', ReactorDesign.reactor_power == 1450)
    )\
    .scalar()
print(result)
```

### Detailed Explanation

1. **Query Construction**:
   - `session.query(func.count(FuelAssembly.id))` selects a scalar count of `FuelAssembly.id`.
   - `.join(ReactorDesign)` and `.join(Epoch)` link the `FuelAssembly` table with `ReactorDesign` and `Epoch`.

2. **Filtering**:
   - The `filter` method applies `Epoch.epoch == 'VD3'` and `ReactorDesign.reactor_power == 1450` to narrow the count to assemblies in the VD3 epoch and reactors of 1450 MWe.

3. **Execution**:
   - The `.scalar()` method executes the query and returns the single count value.

4. **Output**:
   - The integer count is printed, indicating the number of matching fuel assemblies.

### Use Case
This query is useful for generating reports or visualizations that show the relationship between plants and their fuel assemblies. It highlights the power of SQLAlchemy ORM in handling complex relationships with minimal code.

## Potential Enhancements: ETL within ORM Classes

While the current upload script handles bulk insertion, you can improve maintainability and reuse by encapsulating load logic inside ORM classes. For example, add `get_or_create` or `load_from_row` class methods:

```python
class Plant(Base):
    # ...existing code...

    @classmethod
    def get_or_create(cls, session, name: str, location_id: int):
        """Retrieve a Plant by name or create it if not present."""
        plant = session.query(cls).filter_by(plant_name=name).first()
        if not plant:
            plant = cls(plant_name=name, reactor_location_id=location_id)
            session.add(plant)
            session.flush()  # get primary key without commit
        return plant

class FuelAssembly(Base):
    # ...existing code...

    @classmethod
    def load_from_row(cls, session, row):
        """Create a FuelAssembly from a pandas row, linking to related objects."""
        design = ReactorDesign.get_or_create(session, row['reactor_power'], row['reactor_type'])
        plant = Plant.get_or_create(session, row['plant_name'], row['reactor_location_id'])
        epoch = Epoch.get_or_create(session, row['epoch'])
        assembly = cls(
            FA_name=row['FA_name'],
            FA_mass=row['FA_mass'],
            # ...other fields...
            reactor_design_id=design.id,
            plant_id=plant.id,
            epoch_id=epoch.id
        )
        session.add(assembly)
        return assembly
```

### Benefits
- **Separation of Concerns**: Move ETL details into model classes.  
- **Reusability**: Use the same load logic across scripts or tests.  
- **Clarity**: Simplify `upload_data_orm.py` to iterate over CSV rows and call `load_from_row`.

Consider this approach for more robust and maintainable data-loading workflows.
