# CyberWatch — prêt pour GitHub Pages

Portail statique de veille cyber et de suivi des améliorations, issu de l’archive fournie.

## Publication automatique

Le workflow `.github/workflows/pages.yml` publie le site sur GitHub Pages à chaque mise à jour de la branche `main`. Il peut aussi être lancé manuellement depuis l’onglet **Actions**.

1. Créez un dépôt GitHub, par exemple `cyberwatch-portail`, et téléversez le contenu de ce dossier à sa racine.
2. Dans **Settings → Pages**, choisissez **GitHub Actions** comme source de publication.
3. À chaque mise à jour poussée sur `main`, GitHub republiera le site. Son adresse sera `https://TomoAlex.github.io/cyberwatch-portail/` si le dépôt porte ce nom.

Profil GitHub : https://github.com/TomoAlex

## Limites à connaître

- L’application est statique et conserve alertes, suivi et checklist dans le `localStorage` du navigateur. Ces données ne se synchronisent pas entre appareils ou utilisateurs.
- La publication automatique met à jour les fichiers du site. Elle ne collecte pas les nouvelles alertes cyber et ne synchronise pas les données utilisateur en temps réel.
- Pour une collecte périodique de flux (CERT-FR, CISA, NVD) et une synchronisation partagée, il faudra ajouter un service serveur sécurisé, une base de données et des règles d’authentification. Ne mettez jamais de clé API dans `index.html`.
- Les alertes d’octobre 2026 fournies dans l’archive sont des données initiales. Vérifiez leurs sources, dates et versions affectées avant toute utilisation opérationnelle ou publication publique.
- Les données existantes du navigateur ne sont pas incluses dans le dépôt. Utilisez l’export JSON intégré pour les sauvegarder.

## Dépôt privé ou public

Choisissez la visibilité du dépôt selon votre besoin. Le portail contient des exemples d’alertes ; n’y ajoutez aucune donnée sensible de votre organisation si le dépôt est public.

