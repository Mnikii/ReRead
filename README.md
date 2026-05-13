## Install
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirement.txt
```

## Run
```bash
python run.py
```

## Seed locations
```bash
python -m app.scripts.seed_locations
```

## Environment variables
- `SECRET_KEY` - Flask secret (defaults to `dev-secret`)
- `DATABASE_URL` - override database URL

## Swagger / OpenAPI
- Swagger at `/apidocs`


