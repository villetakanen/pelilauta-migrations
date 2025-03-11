# Pelilauta migration scripts

## Running the Migration

Activate your virtual environment:
```zsh
source venv/bin/activate
```

Run the migration script:
```zsh
python migration_scripts/migrate_v1_to_v2.py
```

Run the tests:
```zsh
python -m unittest discover tests
```