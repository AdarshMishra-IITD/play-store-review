# Play Store Review \& Sentiment Dashboard

Search Google Play apps, explore reviews, and moderate user submissions with a supervisor approval workflow, built on Django + PostgreSQL with a fast TF‑IDF + cosine similarity search.

## ✨ What this delivers

- Google‑style search with type‑ahead after 3 characters and ranked results using TF‑IDF + cosine similarity.
- App result pages populated from googleplaystore.csv; review pages populated from googleplaystore_user_reviews.csv.
- Authenticated users submit reviews → pending approval; supervisors log in to approve and publish.


## 🧭 Quick start

Fastest path with Docker:

- Start:

```
docker compose up --build
```

- Reset (fresh DB + containers):

```
docker compose down -v
docker compose up --build
```

- Management command:

```
docker compose exec web python manage.py createsuperuser
```


Local Python:

- Start:

```
pip install -r requirements.txt
python run.py
```

- Custom:

```
python run.py --port 9001
NO_IMPORT=1 python run.py
RUN_HOST=0.0.0.0 RUN_PORT=8080 python run.py
```

- Traditional:

```
python manage.py migrate
python manage.py import_data
python manage.py runserver
```


## 🧩 Core requirements (mapped to features)

- Search experience
    - Suggestions at ≥ 3 chars for instant type‑ahead.
    - Ranked results by text similarity (TF‑IDF + cosine).
- Data mapping
    - App metadata from googleplaystore.csv.
    - App reviews from googleplaystore_user_reviews.csv.
- Review workflow
    - Auth user can submit new review; starts unapproved and hidden.
    - Supervisor can log in, see pending, approve to publish.


## 🔐 Auth \& supervisor role

- Register: /accounts/register/
- Login: /accounts/login/
- Profile: /accounts/profile/
- Supervisor queue: /supervisor/reviews/

Grant supervisor:

```
python manage.py create_supervisor alice --password S3cretPwd --email alice@example.com
```

Revoke:

```
python manage.py create_supervisor alice --remove
```


## 🗄️ Data pipeline

- Raw ingest: playstore/migrations/csv_data/*.csv
- Clean: scripts/clean_data.py → *_clean.csv
- Import: python manage.py import_data (idempotent)
- Persist: Postgres (default) or SQLite
- Present: Django views/templates (search, detail, moderation)


## ⚙️ Configuration

Environment variables:

```
SECRET_KEY=change-me-in-prod
DEBUG=0
ALLOWED_HOSTS=your.host.com,localhost
DJANGO_DB_BACKEND=postgres   # or: sqlite
DJANGO_DB_NAME=playstore_db
DJANGO_DB_USER=playstore_user
DJANGO_DB_PASSWORD=playstore_pass
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5432
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=60
APP_MODE=prod|dev
DEV_PORT=9001
RUN_HOST=0.0.0.0
RUN_PORT=8000
NO_IMPORT=1
```

Tip: Create a .env for local dev and keep it out of VCS.

## 📂 Project layout

```
playstore/               # models, views, urls, mgmt command
  management/commands/import_data.py
project_config/          # settings / wsgi / asgi
scripts/
  clean_data.py          # data cleaning helpers
templates/               # UI templates
docs/                    # detailed documentation
Dockerfile
docker-compose.yml
docker-compose.dev.yml
entrypoint.sh            # container startup logic (dev/prod aware)
run.py                   # local dev bootstrap (migrate/import/run)
```


## 🧪 Testing (planned)

- Models, search ranking, review submission/approval, CSV import.
- tests/ package + CI pipeline to follow.


## 🧭 Common commands

```
python manage.py migrate
python manage.py import_data
python manage.py createsuperuser
python run.py
APP_MODE=dev docker compose up
docker compose up --build
```


## 🛣️ Roadmap

- Semantic embeddings search (SentenceTransformers)
- Pagination and filters (category, rating range)
- Real‑time sentiment for new reviews
- Supervisor analytics dashboard
- Test suite + CI pipeline


## 🙌 Contributing

PRs welcome for search quality, pagination, data normalization, or embeddings prototypes. See CONTRIBUTING.md.

## 📄 License

Add a LICENSE file (e.g., MIT) before external reuse.

## 👤 Author

Adarsh Mishra
adarshmishraiitd@gmail.com
Focus: Generative AI · RAG · LLM Ops · Agent systems