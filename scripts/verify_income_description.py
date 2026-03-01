#!/usr/bin/env python3
"""
Verify that the Income model accepts a description and that the database
schema has the description column.

Usage (model check only, no DB required):
    python scripts/verify_income_description.py

Usage (with live DB check):
    DATABASE_URL=postgresql://... python scripts/verify_income_description.py

Exit codes:
    0 — all checks passed
    1 — one or more checks failed
"""
import re
import sys
import os

# Ensure the project root is on sys.path so app can be imported.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

errors = []

# ── 1. Migration file check ───────────────────────────────────────────────────
migration_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'migrations', 'versions', 'c2d3e4f5g6h7_add_description_to_income.py',
)
if os.path.isfile(migration_path):
    print("✓ Migration file c2d3e4f5g6h7_add_description_to_income.py exists")
else:
    msg = f"Migration file not found: {migration_path}"
    errors.append(msg)
    print(f"✗ {msg}")

# ── 2. Migration content check ───────────────────────────────────────────────
if os.path.isfile(migration_path):
    with open(migration_path) as f:
        content = f.read()
    # Look for add_column('income', ...'description'...) pattern
    if re.search(r"add_column\s*\(\s*['\"]income['\"].*['\"]description['\"]", content, re.DOTALL):
        print("✓ Migration adds 'description' column to 'income' table")
    else:
        msg = "Migration does not appear to add 'description' to 'income'"
        errors.append(msg)
        print(f"✗ {msg}")

# ── 3. Model source check ────────────────────────────────────────────────────
model_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'app', 'models.py',
)
try:
    with open(model_path) as f:
        model_source = f.read()

    income_match = re.search(r'class Income\b.*?(?=\nclass |\Z)', model_source, re.DOTALL)
    if income_match and 'description' in income_match.group(0):
        print("✓ Income model in app/models.py has 'description' field")
    else:
        msg = "Income model in app/models.py is missing 'description' field"
        errors.append(msg)
        print(f"✗ {msg}")
except Exception as exc:
    msg = f"Could not read app/models.py: {exc}"
    errors.append(msg)
    print(f"✗ {msg}")

# ── 4. Database schema check (requires DATABASE_URL) ─────────────────────────
database_url = os.environ.get('DATABASE_URL')
if not database_url:
    print("⚠  DATABASE_URL not set – skipping live database schema check.")
else:
    try:
        from sqlalchemy import create_engine, inspect as sa_inspect

        engine = create_engine(database_url)
        inspector = sa_inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('income')]
        if 'description' in columns:
            print(f"✓ Database 'income' table has 'description' column")
        else:
            msg = f"'description' not in income columns: {columns}"
            errors.append(msg)
            print(f"✗ {msg}")
    except Exception as exc:
        errors.append(f"DB schema check failed: {exc}")
        print(f"✗ DB schema check failed: {exc}")

# ── Result ────────────────────────────────────────────────────────────────────
if errors:
    print(f"\n{len(errors)} check(s) FAILED.")
    sys.exit(1)

print("\nAll checks passed.")
sys.exit(0)
