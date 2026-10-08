# Linux / Docker / DevSecOps — laboratoire de durcissement

**Objectif :** prendre un service HTTP minimal, le placer dans un conteneur Linux et vérifier des protections concrètes. Ce dépôt est un **exercice reproductible**, non un service de production ni une infrastructure cloud déployée.

## Prérequis

Linux ou machine disposant de Docker Engine + Docker Compose v2, Python 3.12+ et curl. Aucun abonnement, compte cloud, secret ou service payant requis.

## Lancer et observer

```bash
# Depuis la racine du dépôt :
python3 -m unittest discover -s labs/hardened-http/tests -v
docker compose -f labs/hardened-http/compose.yaml up -d --build
curl -fsS http://127.0.0.1:8080/health
docker compose -f labs/hardened-http/compose.yaml ps
docker compose -f labs/hardened-http/compose.yaml exec web id
docker compose -f labs/hardened-http/compose.yaml down
```

La commande `bash labs/hardened-http/verify.sh` regroupe les contrôles et arrête le service automatiquement. Une CI vérifie le code, le contrat HTTP et les propriétés Docker.

## Mesures testables

| Mesure | Où | Preuve attendue |
|---|---|---|
| Processus non-root, UID 10001 | Dockerfile, Compose | `docker compose exec web id -u` |
| Suppression des capacités Linux | Compose `cap_drop: ALL` | `docker inspect` |
| Empêcher l'élévation de privilèges | Compose `no-new-privileges` | `docker inspect` |
| Système de fichiers lecture seule | Compose `read_only: true` | Écriture refusée dans `/app` |
| Port local uniquement | Compose `127.0.0.1:8080:8080` | `docker compose ps` |
| Santé vérifiable | `/health` et healthcheck | `curl -f` et `docker compose ps` |
| Automatisation | GitHub Actions | Tests Python + lancement conteneur |

## Exercices à réaliser soi-même

1. Expliquer pourquoi `EXPOSE 8080` ne publie pas le port et pourquoi le binding `127.0.0.1` compte.
2. Tester le refus d'écriture, puis expliquer ce qui changerait si `read_only` était supprimé.
3. Inspecter l'UID, les capacités, `NoNewPrivileges` et `ReadonlyRootfs` ; conserver les sorties expurgées de toute donnée privée.
4. Arrêter le conteneur, constater le changement d'état, puis le relancer.
5. Ajouter dans une prochaine PR une analyse des dépendances et l'épinglage de l'image par digest vérifié.

**Ne pas prétendre maîtriser Docker ou l'avoir déployé en production seulement parce que la CI est verte.** Présenter en entretien les commandes réellement exécutées et leurs résultats.

Voir [THREAT_MODEL.md](THREAT_MODEL.md) pour les limites et risques résiduels.
