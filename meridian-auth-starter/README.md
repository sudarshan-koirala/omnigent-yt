# Meridian Labs - Auth Starter

A tiny Flask API with all authentication logic crammed into a single
`auth.py` (OAuth, JWT, and sessions together). This is intentional.

Use it as the starting point for the Polly demo: ask Polly to refactor
`auth.py` into `oauth.py`, `jwt_utils.py`, and `sessions.py`, and add a
test file for each.

## Run it
    uv venv
    uv pip install flask
    uv run python app.py

Then POST to http://localhost:5000/login with a JSON body like:
    {"email": "jordan.lee@example.com", "password": "anything"}
