# CyberWatch — portail GitHub

Portail statique de veille cyber et de suivi des améliorations, préparé depuis l’archive fournie.

## Déploiement automatique

Le workflow `.github/workflows/pages.yml` publie le site sur GitHub Pages à chaque mise à jour de la branche `main`.

- Dépôt : https://github.com/TomoAlex/CyberWatch
- Site : https://tomoalex.github.io/CyberWatch/
- Les exécutions et leur état sont visibles dans l’onglet **Actions** du dépôt.

## Limites à connaître

- L’application est statique et conserve alertes, suivi et checklist dans le `localStorage` du navigateur. Ces données ne se synchronisent pas entre appareils ou utilisateurs.
- La publication automatique met à jour les fichiers du site. Elle ne collecte pas de nouvelles alertes cyber et ne synchronise pas les données utilisateur en temps réel.
- Pour une collecte périodique de flux (CERT-FR, CISA, NVD) et une synchronisation partagée, il faudra ajouter un service serveur sécurisé, une base de données et des règles d’authentification. Ne mettez jamais de clé API dans `index.html`.
- Les alertes d’octobre 2026 présentes dans l’archive sont des données initiales. Vérifiez leurs sources, dates et versions affectées avant toute utilisation opérationnelle.
- Le dépôt est public. N’y ajoutez aucune donnée sensible de votre organisation.
- Les données du navigateur ne sont pas incluses dans le dépôt. Utilisez l’export JSON intégré pour les sauvegarder.

