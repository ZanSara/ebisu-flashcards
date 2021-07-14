# Flashcards API - WIP

Flashcards REST API.

**NOTE**: This is a work-in-progress, not running application. 
Do not expect it to just download it and be able to run it if you're not
familiar with Python.

## Run development server

```bash
> cd backend
> python3 -m venv venv
> source venv/bin/activate
> pip install .

[ ... pip logs ... ]

> uvicorn flashcards_api.main:app

INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:60494 - "GET / HTTP/1.1" 200 OK
```

## OpenAPI Docs

Visit either `127.0.0.1:8000/docs` or `127.0.0.1:8000/redoc`.