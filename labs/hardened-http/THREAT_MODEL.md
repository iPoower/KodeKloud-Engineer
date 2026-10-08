# Threat model simplifié — laboratoire HTTP

## Actifs
Processus de service, image de conteneur, intégrité du code, disponibilité locale. Aucune donnée utilisateur réelle ni secret n'est nécessaire.

## Adversaires et contre-mesures

- **Client externe au poste :** port publié sur loopback uniquement. Risque résiduel : proxy, reverse-proxy ou paramétrage réseau ajouté ensuite.
- **Entrée HTTP malveillante :** routes en liste fermée et réponses JSON constantes ; serveur standard-library, pas de rendu HTML. Risque résiduel : `http.server` n'est pas un serveur web durci pour Internet.
- **Processus compromis :** UID non-root, `cap_drop: ALL`, `no-new-privileges`, système de fichiers lecture seule, limites mémoire/processus. Cela ne remplace ni un isolement VM ni un correctif du noyau.
- **Image compromise :** base officielle Python mais tag versionné, non épinglé par digest ; mettre à jour et vérifier le digest, scanner l'image et tenir la dépendance à jour avant réutilisation.
- **Indisponibilité :** Docker healthcheck, aucun mécanisme de redondance ni alerting externe ; seulement une preuve de concept locale.
- **CI :** permissions minimales, exécution sans secrets. Les runners Github ne prouvent pas que le service est sécurisé contre des attaquants réels.

## Périmètre et preuves

Les tests vérifient la réponse HTTP, un UID non-root et l'impossibilité d'écrire dans `/app`. Pour vérifier les options Linux effectives : inspecter `HostConfig.CapDrop`, `HostConfig.SecurityOpt`, `HostConfig.ReadonlyRootfs` avec `docker inspect`. Tester manuellement sur Linux et conserver un court compte rendu avant toute affirmation sur son exploitation.

**Ne pas publier le service sur Internet.** Pas de TLS, d'authentification, de rate limiting ni de patch-management automatisé au-delà du workflow d'exercice.
