# Star Wars API

This is a small REST API built with Django and Django REST Framework. It fetches characters, films, and starships from [SWAPI](https://swapi.dev/), stores them in a local SQLite database, and lets users browse, search, and vote for their favourites.

## Main features

- Import characters, films, and starships from SWAPI
- Store the imported data in SQLite
- Keep character-to-film and starship-to-film relationships
- List the stored resources with pagination
- Search characters, films, and starships
- Vote for a character, film, or starship
- Graceful handling of SWAPI timeouts and invalid responses
- Interactive API documentation with Swagger
- Tests that mock calls to the external API

## Technologies used

- Python 3
- Django
- Django REST Framework
- drf-spectacular
- SQLite
- Requests
- Coverage.py

## Setup

Clone the repository and move into the project directory:

```bash
git clone https://github.com/konstantinosvlachakis/starwars.git
cd starwars
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies and apply the migrations:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## Importing data from SWAPI

The data can be imported with the management command:

```bash
python manage.py import_swapi
```

It can also be imported through the API:

```bash
curl -X POST http://127.0.0.1:8000/api/import/
```

The import uses `update_or_create`, so running it again updates existing records instead of creating duplicates.

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/import/` | Fetch and store all supported resources from SWAPI |
| `GET` | `/api/characters/` | List stored characters |
| `GET` | `/api/films/` | List stored films |
| `GET` | `/api/starships/` | List stored starships |
| `POST` | `/api/characters/{id}/vote/` | Vote for a character |
| `POST` | `/api/films/{id}/vote/` | Vote for a film |
| `POST` | `/api/starships/{id}/vote/` | Vote for a starship |

List endpoints are paginated with 10 results per page. For example:

```text
/api/characters/?page=2
```

Use the `search` query parameter to filter the results:

```text
/api/characters/?search=Luke
/api/films/?search=Empire
/api/starships/?search=Falcon
```

Starships can be searched by both name and model. Films are searched by title.

## API documentation

After starting the server, the Swagger UI is available at:

```text
http://127.0.0.1:8000/api/swagger/
```

The generated OpenAPI schema is available at:

```text
http://127.0.0.1:8000/api/schema/
```

## Tests and coverage

Run the test suite with:

```bash
python manage.py test
```

To run the tests and measure coverage:

```bash
coverage run --source=swapi --omit=swapi/tests.py,swapi/migrations/* manage.py test
coverage report -m
```

The current test suite contains 28 tests and reports 91% coverage of the application code.

An HTML coverage report can also be generated:

```bash
coverage html
```

The report will be created in `htmlcov/index.html`. On Windows, it can be opened from PowerShell with:

```powershell
Start-Process ".\htmlcov\index.html"
```

An XML coverage report can be generated for CI tools or submission with:

```bash
coverage xml -o coverage.xml
```

The XML file can be opened in VS Code:

```powershell
code coverage.xml
```

or in the default browser on Windows:

```powershell
Start-Process ".\coverage.xml"
```

The XML report is intended mainly for automated tools. The HTML report is more convenient for viewing coverage details manually.
