# French Nuclear Fuel Assembly Data Project

## Project Objectives & Pedagogical Goals

This project demonstrates the design, normalization, and querying of a synthetic French nuclear fuel assembly dataset using Python (pandas), SQL (SQLite3/Oracle), and SQLAlchemy Core. It is intended as a pedagogical resource for understanding the differences between denormalized flat files and normalized relational database schemas, as well as for illustrating best practices in ETL, schema design, and query formulation.

---

## 1. Data Generation and Structure
- Synthetic, pedagogical nuclear fuel assembly data is generated using `data/generate_raw_data.py`.
- The script uses `pathlib` for robust, relative file handling and always outputs to the top-level `data/` directory.
- The generated files are `plants_data.csv` and `plants_data.xlsx`, with intentionally denormalized, pedagogical column names (e.g., `FA_mass_kg`, `region`, `plant_code`, etc.) as described in `data/domain_rules.txt`.

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

**This project is fully reproducible, tested, and ready for further extension or teaching.**
