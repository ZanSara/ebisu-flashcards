# Ebisu Flashcards - WIP

Flashcards application based on the Ebisu algorithm.

**NOTE**: This is a work-in-progress, not running application. 
Do not expect it to just download it and be able to run it if you're not
familiar with Python and React/NodeJS.

## Run backend

```bash
> cd backend
> python3 -m venv venv
> source venv/bin/activate
> pip install .

[ ... pip logs ... ]

> ebisu

 * Serving Flask app "ebisu_flashcards.app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:3501/ (Press CTRL+C to quit)
 * Restarting with stat
```

## Run frontend

```bash
> cd frontend
> npm install

[ ... npm logs ... ]

> npm dev run

   > ebisu-web@0.1.0 dev /path/to/project/ebisu-flashcards/frontend
   > next dev
```