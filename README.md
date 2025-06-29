# French Nuclear Fuel Assembly Data Project

## Project Objectives & Pedagogical Goals

This project demonstrates the design, normalization, and querying of a synthetic French nuclear fuel assembly dataset using Python (pandas), SQL (SQLite3/Oracle), and SQLAlchemy Core and ORM. It is intended as a pedagogical resource for understanding the differences between denormalized flat files and normalized relational database schemas, as well as for illustrating best practices in ETL, schema design, and query formulation.

---

Readers are encouraged to go through the chapters step by step to fully understand the project.

## 1. Data Generation and Structure


This section concerns the `/data` folder, which contains:

- **`generate_raw_data.py`**: Python script for generating synthetic nuclear fuel assembly data.
- **`plants_data.csv`**: Denormalized CSV file containing the generated data.
- **`plants_data.xlsx`**: Denormalized Excel file containing the generated data.
- **`domain_rules.md`**: Markdown file detailing the business and data integrity rules for the dataset.
- **`plants_data.xlsx` and `plants_data.csv`**: Generated data files with pedagogical column names (e.g., `FA_mass_kg`, `region`, `plant_code`, etc.).
- **`UML Database Relationship.pdf`**: A PDF file describing class diagrams in UML (a standard software design description approach). Such diagrams include objects (attributes, methods) and the relationships between these objects, providing a clear representation of a computer program structure.
- **`FA_AC_FA5506.xml`**: A sample XML file providing detailed information about a specific fuel assembly, including grids, nozzle, fuel rods, and plant introduction details.

## 2. Bibliography

The `/bibliography` folder contains reference materials and review articles related to database design, SQL, and data modeling. These resources provide theoretical and practical insights into relational databases and their applications. Key files include:

- **`A Relational Model of Data for Large Shared Data Banks (E. F. Codd).pdf`**: A seminal paper introducing the relational model of data.
- **Other reference materials**: Books that support the pedagogical goals of the project.

## 3. Pandas Queries and Philosophy

The `/pandas` folder contains scripts and documentation that demonstrate querying denormalized data using pandas. Key files include:

- **`query_examples_pandas.py`**: A Python script showcasing example queries on the flat CSV data, highlighting the challenges and verbosity of pandas compared to SQL.
- **`pandas_vs_sql_query_philosophy.md`**: A Markdown document comparing the query philosophy of SQL and pandas, emphasizing the advantages of normalization and SQL JOINs versus the manual effort required in pandas for similar tasks.

## 4. SQL Dialects

The `/SQL` folder contains SQL scripts, schema comparisons, and documentation for both SQLite3 and Oracle. Key files include:

- **`sqlite_vs_oracle_schema_comparison.md`**: A Markdown file comparing schema design and syntax between SQLite3 and Oracle, using the nuclear fuel assembly dataset as an example.
- **`entity_relation_scheme/SQL_sqlite3_entity_relation_scheme.png`**: A PNG file illustrating the entity-relationship diagram for the SQLite3 schema.

Subfolders:

- **`sqlite3/`**: Contains SQLite3-specific scripts and schema files.
- **`oracle/`**: Contains Oracle-specific scripts and schema files.

## 5. Query Demonstrations
- Example queries for both SQLite3 and Oracle are provided in their respective folders.
- `pandas/query_examples_pandas.py` demonstrates how queries are more verbose and error-prone on the flat CSV using pandas.
- `SQLAlchemy_core/query_examples_core.py`:
  - Loads the denormalized CSV.
  - Explicitly normalizes the data (with pedagogical comments and column mapping).
  - Populates an in-memory SQLite database using SQLAlchemy Core.
  - Runs a set of analytical queries, using correct SQLAlchemy aggregation functions (`func.max`, `func.min`).
  - All column names and mappings are now consistent with the generated CSV and the domain rules.

## 6. SQLAlchemy Core

The `/SQLAlchemy_core` folder contains scripts demonstrating the use of SQLAlchemy Core for defining tables and executing queries. Key files include:

- **`fuel_assembly_core_demo_full.py`**: Defines SQLAlchemy Core table schemas for a normalized database structure, including tables like `REACTOR_DESIGN`, `PLANTS`, `EPOCHS`, `REACTOR_LOCATIONS`, and `FUEL_ASSEMBLY`. Generates `CREATE TABLE` statements for both SQLite3 and Oracle.
- **`query_examples_core.py`**: Contains example queries using SQLAlchemy Core to interact with the database. Demonstrates how to perform operations like data insertion, selection, and aggregation.
- **`sqlalchemy_core_summary.md`**: A Markdown file summarizing the SQLAlchemy Core approach, highlighting identical table creation and query execution for SQLite and Oracle, with examples of the `FUEL_ASSEMBLY` table definition and queries.

## 7. SQLAlchemy ORM

The `/SQLAlchemy_ORM` folder contains three scripts demonstrating the use of SQLAlchemy ORM:

1. `create_tables_orm.py`: Defines the ORM models and creates the SQLite database tables.
2. `upload_data_orm.py`: Uploads data from the `plants_data.csv` file into the SQLite database using the ORM models.
3. `query_data_orm.py`: Executes the same queries as in the SQLAlchemy Core example, but using the ORM approach.

## 8. Presentation

The `/presentation` folder contains materials designed for teaching and presenting the concepts covered in this project.

- **`ORM_SQLAlchemy_PyCoD_LEBAIL_062025_01.pptm`**: The presentation held in PyCoD online monthly meeting on 04/07/2025.
- **`material/`**: Supporting images and graphics used in the presentation

---

## Contact
For further inquiries, please contact:

**Hervé LEBAIL**  
FDM2-E, Framatome  
herve.lebail@framatome.com

---

**Special Thanks**: This project benefited from insights provided by ChatGPT, an AI assistant. For similar questions or assistance, consider using ChatGPT to explore and solve complex problems efficiently. Everything here is public domain data (C0 classification) and even fake, for the sole purpose of the topic demonstration. At FRAMATOME feel free to use GenAI (C1 classification).

---

**This project is fully reproducible, tested, and ready for further extension or teaching.**
