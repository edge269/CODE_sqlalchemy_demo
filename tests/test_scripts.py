import subprocess
from pathlib import Path
import pytest
import sys  # use the current interpreter (e.g., venv) for subprocess calls

# List of scripts to test (relative to project root)
SCRIPTS = [
    Path('data/generate_raw_data.py'),
    Path('pandas/query_examples_pandas.py'),
    # SQLAlchemy Core scripts
    Path('SQLAlchemy_core/fuel_assembly_core_demo_full.py'),  # create core tables and data first
    Path('SQLAlchemy_core/query_examples_core.py'),  # then run core query examples
    # ORM scripts
    Path('SQLAlchemy_ORM/create_tables_orm.py'),
    Path('SQLAlchemy_ORM/upload_data_orm.py'),
    Path('SQLAlchemy_ORM/query_data_orm.py'),
]

@pytest.mark.parametrize("script_path", SCRIPTS)
def test_script_runs(script_path):
    """Test that a script runs without error (exit code 0)."""
    script_abs = Path(__file__).resolve().parent.parent / script_path
    # invoke the same Python interpreter that runs pytest (ensures venv packages are available)
    result = subprocess.run([sys.executable, str(script_abs)], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with error:\n{result.stderr}"
