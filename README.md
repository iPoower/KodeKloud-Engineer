# KodeKloud Engineer — exercices Linux et DevSecOps

Dépôt d'apprentissage. Chaque exercice distingue ce qui est **écrit dans le code**, **testé automatiquement** et **encore à valider manuellement**.

## Exercices

- [Créer un utilisateur Linux](./1%20Create%20a%20user) — commande SSH sans secret intégré ni désactivation du contrôle de clé hôte.
- [Lab Docker : microservice Linux durci](labs/hardened-http/) — service Python standard-library, conteneur non-root, système de fichiers en lecture seule, capacités Linux supprimées, contrôle de santé et tests automatisés.

## Vérifications rapides

```bash
python3 -m unittest discover -s labs/hardened-http/tests -v
docker compose -f labs/hardened-http/compose.yaml config --quiet
bash labs/hardened-http/verify.sh
```

Docker et Docker Compose sont nécessaires pour la vérification du conteneur. **Ce lab n'est pas déployé sur Internet**, ne demande aucun compte cloud ni service payant et ne constitue pas une preuve d'exploitation de production.

## Hygiène de sécurité

Un ancien exercice versionné contenait un mot de passe de laboratoire en clair et désactivait le contrôle de l'identité SSH. Il est retiré de la version courante, **mais les anciens commits restent consultables** : ne jamais réutiliser de tels secrets et les révoquer s'ils étaient valides.
