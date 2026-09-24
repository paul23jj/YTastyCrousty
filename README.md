# YTastyCrousty

## Description

Projet de deuxième année d'informatique : une API REST pour les restaurants Ytasty Crousty d'Aix, Lyon et Paris. Les clients peuvent passer et suivre leurs commandes, et les employés gérer les restaurants et les produits selon leurs droits.

## Fonctionnalités

- Connexion par JWT, création des utilisateurs et rôles admin, staff et direction.
- Initialisation automatique des trois restaurants et du compte administrateur.
- Consultation des restaurants et modification de leurs informations par un administrateur.
- Recherche des produits avec filtres, création, modification, suppression et disponibilité.
- Commandes publiques, calcul du total côté serveur, suivi, statuts et annulation.
- Contrôle des accès par restaurant et documentation Swagger avec authentification Bearer.

## Technologies

Python 3.11+, FastAPI et Uvicorn pour l'API ; PostgreSQL, SQLAlchemy et Psycopg pour les données ; Pydantic pour la validation ; Passlib avec PBKDF2-SHA256 et PyJWT pour l'authentification ; uv et Docker Compose pour l'installation.

`email-validator` est utilisé par le type `EmailStr` de Pydantic pour vérifier l'adresse du client d'une commande.

## Pré-requis

Git, Docker et Docker Compose. Docker doit être démarré et les ports `8000` et `5432` disponibles. Python et les dépendances sont installés dans l'image Docker. Hors de Docker, installer aussi uv et utiliser `uv sync --locked` pour installer les dépendances.

## Installation et lancement

Commandes PowerShell :

```powershell
git clone https://github.com/paul23jj/YTastyCrousty.git
cd YTastyCrousty
Copy-Item .env.example .env
```

Renseigner `SECRET_KEY` dans `.env` avec une clé aléatoire privée d'au moins 32 caractères. Garder `ADMIN_PASSWORD=Admin@123456` pour le compte imposé par le sujet. Ne pas ajouter `.env` dans Git.

```powershell
docker compose up --build
```

La base PostgreSQL, les tables, les trois restaurants et l'administrateur sont initialisés automatiquement. Aucun script SQL n'est à exécuter manuellement. Les données sont conservées entre deux démarrages.

- [État de l'API](http://localhost:8000/health)
- [Swagger](http://localhost:8000/docs)
- [OpenAPI](http://localhost:8000/openapi.json)

Dans Swagger, utiliser `POST /auth/login` avec `admin123` et `Admin@123456`, puis coller le token reçu dans **Authorize**. Le compte admin imposé est une exception à la longueur minimale de 12 caractères appliquée aux nouveaux comptes.

Pour arrêter : `docker compose down`. Modifier `ADMIN_PASSWORD` ne change pas un mot de passe déjà enregistré en base.

Pour l'accès HTTPS prévu avec ngrok, installer et connecter ngrok à son compte en suivant la [documentation officielle](https://ngrok.com/docs/share-localhost/quickstart), puis lancer dans un autre terminal :

```powershell
ngrok http 8000
```

Transmettre à l'enseignant l'adresse HTTPS affichée et cette même adresse suivie de `/docs`. Vérifier également `/health` et `/openapi.json` depuis l'adresse publique. Docker, ngrok et l'ordinateur doivent rester en fonctionnement pendant toute la correction ; une adresse publique permanente reste à valider avant la remise.

## Répartition des tâches

Nous avons réparti nos tâches avec un Kanban dans GitHub Projects en laissant à chacun le choix de ses tâches. Les [issues GitHub](https://github.com/paul23jj/YTastyCrousty/issues) permettent de suivre leur avancement. Nous travaillons sur des branches dédiées avant d'intégrer les fonctionnalités sur `dev`.

## Contributeurs

- [Paul](https://github.com/Florian-AZ)
- [Harold](https://github.com/Emrick-R)
- [Leyth](https://github.com/Leyth07)