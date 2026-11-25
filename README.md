# CyberWatch — portail GitHub

Portail statique de veille cyber et de suivi des améliorations, préparé depuis l’archive fournie.

## Déploiement automatique

Le workflow `.github/workflows/pages.yml` publie le site sur GitHub Pages à chaque mise à jour de la branche `main`.

- Dépôt : https://github.com/TomoAlex/CyberWatch
- Site : https://tomoalex.github.io/CyberWatch/
- Les exécutions et leur état sont visibles dans l’onglet **Actions** du dépôt.

## Limites à connaître

- L’application est statique et conserve alertes, suivi et checklist dans le `localStorage` du navigateur. Ces données ne se synchronisent pas entre appareils ou utilisateurs.
- Le workflow GitHub Actions récupère le flux RSS officiel des alertes CERT-FR toutes les 15 minutes et republie le site avec un instantané `alerts.json`. Le portail charge cet instantané à l’ouverture, lors d’une actualisation manuelle et toutes les 15 minutes dans un onglet ouvert.
- Les alertes importées sont fusionnées avec les données locales ; les suivis déjà saisis dans ce navigateur sont conservés. Le flux fournit des signaux à qualifier, pas une analyse de votre inventaire informatique.
- La collecte périodique de CISA, NVD ou d’autres éditeurs, ainsi que la synchronisation des données entre utilisateurs, demanderaient des intégrations supplémentaires et un service sécurisé. Ne mettez jamais de clé API dans `index.html`.
- Les alertes d’octobre 2026 présentes dans l’archive sont des données initiales. Vérifiez leurs sources, dates et versions affectées avant toute utilisation opérationnelle.
- Le dépôt est public. N’y ajoutez aucune donnée sensible de votre organisation.
- Les données du navigateur ne sont pas incluses dans le dépôt. Utilisez l’export JSON intégré pour les sauvegarder.

