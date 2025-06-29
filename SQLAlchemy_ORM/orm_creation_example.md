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

### Example Code

Below is a simplified example of how data is uploaded:

```python
# Clear existing data
session.query(FuelAssembly).delete()
session.query(Plant).delete()
session.commit()

# Read CSV data
import pandas as pd
csv_path = Path(__file__).parent / 'plants_data.csv'
data = pd.read_csv(csv_path)

# Insert data
for _, row in data.iterrows():
    plant = Plant(
        plant_name=row['plant_name'],
        reactor_location_id=row['reactor_location_id']
    )
    session.add(plant)

session.commit()
print("Data uploaded successfully.")
```

## Query Example

The query script (`query_data_orm.py`) retrieves data from the database. Below is an example of Query 4:

### Query 4: Retrieve Plants and Their Fuel Assemblies

This query retrieves all plants along with their associated fuel assemblies. It demonstrates how to use SQLAlchemy ORM to query relational data efficiently.

```python
results = session.query(Plant).join(FuelAssembly).all()
for plant in results:
    print(f"Plant: {plant.plant_name}")
    for assembly in plant.fuel_assemblies:
        print(f"  Fuel Assembly: {assembly.FA_name}, Mass: {assembly.FA_mass}")
```

### Detailed Explanation

1. **Query Construction**:
   - The `session.query(Plant)` starts the query by selecting the `Plant` table.
   - The `.join(FuelAssembly)` method specifies an inner join between the `Plant` and `FuelAssembly` tables based on their relationship.

2. **Execution**:
   - The `.all()` method executes the query and retrieves all matching rows.

3. **Iteration**:
   - The results are iterated using a `for` loop.
   - For each `Plant` object, the `plant_name` attribute is printed.
   - The `fuel_assemblies` relationship is accessed to retrieve associated `FuelAssembly` objects.

4. **Output**:
   - For each `FuelAssembly` object, the `FA_name` and `FA_mass` attributes are printed.

### Use Case
This query is useful for generating reports or visualizations that show the relationship between plants and their fuel assemblies. It highlights the power of SQLAlchemy ORM in handling complex relationships with minimal code.
