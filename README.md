# README

## Start services

## Backend

To build the container:
```bash
docker build -f Dockerfile -t marches-publics-backend .
```

To start the container standalone:

```bash
docker run --rm -p 5001:5001 marches-publics-backend
```

## Frontend

To build the container (from the ui folder):
```bash
docker build -f Dockerfile -t marches-publics-frontend .
```

To start the container standalone:

```bash
docker run --rm -p 3000:3000 marches-publics-frontend
```

## Full service

To start both containers:
```bash
sudo docker-compose up --detach
```

## Resources

- https://doc.data.gouv.fr/api/intro/
- https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-fichiers-consolides/
