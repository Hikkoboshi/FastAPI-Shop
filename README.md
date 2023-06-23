# FastAPI Shop

At this project I'm learning FastAPI. Hope I can make good API for e-commerce

## Roadmap
1. Code and project refactoring
2. User auth and auth dependencies
3. Expand API capabilities
4. Add AJAX requests
5. Change frontend (templates > Vue.js)
6. And more...

## Usage
If you use **PostgreSQL** and run project locally, you can follow this instruction

- [Run project locally with PostgreSQL](#local)
- [Docker](#docker)

***Don't use included .env file at production!***
***
### Local
Install requirements
```bash
pip install -r requirements.txt
```

Make migrations
```bash
alembic init migrations
alembic revision --autogenerate
alembic upgrade head
```

Run the project
```bash
uvicorn main:app --reload
```

Now you can use it, but if you have errors, I'm sorry

If you want to fill your database with categories and products, execute /fetch_fake_catalog at the http://localhost:8000/docs


### Docker
Either you want to use **Docker** - follow this instruction

***First change DB_HOST in .env file to database (or to other if you've changed name of service in docker-compose.yml)***

Build and run the project with docker-compose
```bash
docker-compose up -d --build
```

After your containers up, make migrations for database. You can do it from **database container** or from **terminal**
```bash
# From database container
alembic init migrations
alembic revision --autogenerate
alembic upgrade head
# From terminal
docker-compose exec -it backend alembic init migrations
docker-compose exec -it backend alembic revision --autogenerate
docker-compose exec -it backend alembic upgrade head
```

