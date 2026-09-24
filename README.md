# Ytasty Crousty API

API REST du projet Ytasty Crousty, développée avec FastAPI, SQLAlchemy et PostgreSQL.

## Prérequis

- Docker et Docker Compose

## Lancement local

1. Copier `.env.example` vers `.env`.
2. Remplacer `SECRET_KEY` par une valeur locale non publiée.
3. Lancer `docker compose up --build`.

L'API est ensuite disponible aux adresses suivantes :

- API : `http://localhost:8000`
- Santé : `http://localhost:8000/health`
- Swagger : `http://localhost:8000/docs`
- OpenAPI : `http://localhost:8000/openapi.json`

Le compte administrateur demandé par le sujet est créé automatiquement au premier démarrage.

## Configuration

Les variables nécessaires sont décrites dans `.env.example` :

- `DB_URL` : URL de connexion SQLAlchemy à PostgreSQL ;
- `ADMIN_PASSWORD` : mot de passe initial du compte `admin123` ;
- `SECRET_KEY` : clé utilisée pour signer les jetons JWT ;
- `ALGORITHM` et `ACCESS_TOKEN_EXPIRE_MINUTES` sont facultatives et disposent de valeurs par défaut.

Le fichier `.env` contient les valeurs locales et ne doit jamais être ajouté à Git.
