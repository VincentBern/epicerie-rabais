# Procédure hebdomadaire (tâche du jeudi, session non supervisée)

Remplace les parties du skill `maxi-flyer-deals` qui dépendent de `db_get`/`db_write` (absents des sessions nuage) et de `SendUserMessage`. Le reste du skill (règles, critères de vrai deal, format du tableau 3 colonnes) s'applique.

## Historique
- L'historique est le dossier `data/*.json` de ce dépôt (un fichier par semaine, nom = jeudi de début). Ne pas utiliser l'artefact ni `db_*`.
- Avant de juger les deals: lire tous les `data/*.json`, comparer à la médiane et au plus bas par produit et par épicerie. Moins de 4 semaines: le dire.
- Réutiliser exactement les noms de produit `p` des semaines précédentes.
- Si `data/<jeudi de début>.json` existe déjà avec plusieurs épiceries, le compléter plutôt que le refaire.

## Sources
- Réseau: l'environnement « epicerie » autorise metro.ca, superc.ca, provigo.ca, maxi.ca, iga.net, circulaires.club, circulairecanada.com, circulaire-en-ligne.ca, kimbino.ca.
- WebFetch peut échouer (ENOTFOUND) même pour un hôte autorisé: utiliser alors `curl -sL` dans Bash avec le User-Agent par défaut (jamais un faux User-Agent de navigateur; ne pas contourner un 403), écrire dans le scratchpad, puis extraire le texte.
- Metro, Provigo, Super C: les sites officiels n'ont pas de prix en texte (superc.ca répond 403). Source: circulaires.club (/magasin/metro/, /magasin/provigo/, /magasin/super-c/, section « Les aubaines ... de la semaine »). Corroborer avec circulairecanada.com / circulaire-en-ligne.ca; sinon `note: "une seule source (circulaires.club)"` et `?` sans 🔥.
- Maxi: maxi.ca (voir le skill). IGA: flyers.iga.net grid_view + tiers.
- Provigo n'a pas de circulaire dans la Capitale-Nationale selon circulaires.club: le dire, offres à valider pour Québec. Adonis: une seule tentative, sinon vide.

## Collecte complète + drapeau « recommandé »
- Relever TOUS les aliments en rabais de chaque circulaire consultée, pas seulement les bons deals (exclure seulement le non alimentaire: papier, ménage, soins, animaux). Même nom `p` d'une semaine à l'autre pour un même produit.
- Ensuite, marquer `"rec": true` (au niveau du produit, pas de l'épicerie) sur ceux qui valent vraiment la peine: rabais d'environ 25 % ou plus par rapport au prix régulier, ou prix à l'unité exceptionnellement bas / plus bas de l'historique pour un aliment de base. Sans prix régulier (Metro, Provigo, Super C): `rec` pour les aliments de base à prix bas. Un prix d'une seule source peut être `rec` mais garde sa note « une seule source » et pas de 🔥. Pas de `rec` pour plats préparés, boissons, collations sans vrai rabais.
- La page affiche par défaut seulement les `rec` (bouton « ★ Recommandés »); « Tous les spéciaux » montre le reste. Une semaine sans aucun `rec` s'affiche au complet.
- Le message final (tableau 3 colonnes) ne contient que les `rec`; la ligne de couverture donne le total relevé par épicerie et le nombre de recommandés.

## Publication (obligatoire, avant la notification)
1. Écrire/mettre à jour `data/<AAAA-MM-JJ>.json` (format dans README.md; clés maxi, iga, metro, provigo, superc, adonis; commentaire = sources réellement consultées).
2. `python3 build_page.py`; vérifier que index.html contient metro, provigo, superc.
3. Commit « Semaine du <date> », puis `git push origin HEAD:main` ET `git push -u origin <branche de la session>`. Si un push échoue, copier l'erreur exacte.

## Message final
- Pas de `SendUserMessage`: utiliser PushNotification avec `<routine_summary>`: tableau compact 3 colonnes, verdict, détour, dates, couverture, hash du commit et lien https://vincentbern.github.io/epicerie-rabais/.
- En cas d'échec (source bloquée, push refusé), notifier aussi, avec l'erreur exacte.
