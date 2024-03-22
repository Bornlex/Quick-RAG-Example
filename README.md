# README

## Start services

```bash
docker-compose up
```

## Backend

To build the container:
```bash
docker build -f Dockerfile -t marches-publics-backend .
```

To start the container:

```bash
docker run --rm -p 5000:5000 marches-publics-backend
```

## Frontend

To build the container (from the ui folder):
```bash
docker build -f Dockerfile -t marches-publics-frontend .
```

To start the container:

```bash
docker run --rm -p 3000:3000 marches-publics-frontend
```

## Resources

- https://doc.data.gouv.fr/api/intro/
- https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-fichiers-consolides/
