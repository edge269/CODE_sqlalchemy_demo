# Test Suite Overview

This directory contains automated tests that verify key project scripts run successfully without errors.

## tests/test_scripts.py

- Uses `pytest` to parameterize a list of script paths (`SCRIPTS`).
- For each script, constructs an absolute path and invokes it as a subprocess using the same Python interpreter that runs the tests (`sys.executable`).
- Captures `stdout` and `stderr` and asserts the script exits with return code `0`.

### Scripts Tested

1. **Data Generation**: `data/generate_raw_data.py` generates raw CSV and databases.
2. **Pandas Queries**: `pandas/query_examples_pandas.py` demonstrates data analysis using Pandas.
3. **SQLAlchemy Core**: 
   - `SQLAlchemy_core/fuel_assembly_core_demo_full.py` defines and prints DDL statements.
   - `SQLAlchemy_core/query_examples_core.py` runs SQL Core queries against in-memory and file-based SQLite, skipping Oracle.
4. **ORM Scripts**:
   - `SQLAlchemy_ORM/create_tables_orm.py` creates the ORM-based tables.
   - `SQLAlchemy_ORM/upload_data_orm.py` loads CSV data into the ORM tables.
   - `SQLAlchemy_ORM/query_data_orm.py` runs ORM-based queries and prints results.

## Setting Up the Python Environment

Before running tests, install project dependencies in a clean environment. Choose one of the following approaches:

### Using venv (recommended)
```bash
# Create a virtual environment
python3 -m venv venv
# Activate the environment
source venv/bin/activate
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Using Conda (optional)
```bash
# Create a new conda environment
conda create -n sqlalchemy-demo python=3.12 -y
# Activate the environment
conda activate sqlalchemy-demo
# Install dependencies
pip install -r requirements.txt
```

## Running Tests

1. **Install dependencies**: Ensure `pytest` is installed in the virtual environment.
2. **Activate environment**:
   ```bash
   source venv/bin/activate
   ```
3. **Run tests**:
   ```bash
   pytest tests/test_scripts.py -q
   ```

All tests must pass, confirming that scripts execute without errors in the configured environment.
