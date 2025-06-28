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
- **`generate_raw_db.py`**: Script for generating raw database structures.
- **`plants_data.xlsx` and `plants_data.csv`**: Generated data files with pedagogical column names (e.g., `FA_mass_kg`, `region`, `plant_code`, etc.).
- **`Uml Database Relationship.pdf`**: A PDF file describing class diagrams in UML (a standard software design description approach). Such diagrams include objects (attributes, methods) and the relationships between these objects, providing a clear representation of a computer program structure.

## 2. Schema Normalization and Documentation
- SQL schemas for both SQLite3 and Oracle are designed and normalized, with DDL and DBML in the `SQL/` directory.
- Markdown documentation and DBML diagrams compare normalized and denormalized structures, and explain the pedagogical intent.

## 3. Query Demonstrations
- Example queries for both SQLite3 and Oracle are provided in their respective folders.
- `pandas/query_examples_pandas.py` demonstrates how queries are more verbose and error-prone on the flat CSV using pandas.
- `SQLAlchemy_core/query_examples_core.py`:
  - Loads the denormalized CSV.
  - Explicitly normalizes the data (with pedagogical comments and column mapping).
  - Populates an in-memory SQLite database using SQLAlchemy Core.
  - Runs a set of analytical queries, using correct SQLAlchemy aggregation functions (`func.max`, `func.min`).
  - All column names and mappings are now consistent with the generated CSV and the domain rules.

## 4. Testing and Automation
- A `tests/` folder contains `test_scripts.py`, which uses `pathlib` and subprocess to check that all main scripts (data generation, pandas, SQLAlchemy Core) run without error.
- All scripts now pass these tests.

## 5. Version Control
- All changes are tracked and committed in git.
- The latest state is pushed to the remote repository.

## 6. Pedagogical Consistency
- All code, documentation, and data files are now consistent with the pedagogical goals:
  - Clear distinction between denormalized (flat) data and normalized relational schema.
  - Explicit mapping and normalization steps.
  - Comments and documentation reference the business/domain rules for clarity.

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
