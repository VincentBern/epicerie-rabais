# Rabais d'épicerie – région de Québec

Comparaison hebdomadaire des circulaires (Maxi, IGA, Metro, Provigo, Super C, Adonis), publiée avec GitHub Pages. Pensée pour le téléphone.

Dans la page: choix des épiceries (mémorisé sur l'appareil, 4 à la fois), recherche d'un aliment, navigation par semaine, et fiche par produit avec l'historique de son prix.

## Fichiers

- `data/AAAA-MM-JJ.json`: données d'une semaine (une ligne par produit)
- `build_page.py`: génère `index.html` (toutes les semaines intégrées) et `archive/` (redirections vers `index.html#AAAA-MM-JJ`)

## Format d'une semaine

```json
{"start": "2026-11-05", "end": "2026-11-11", "comment": "…",
 "items": [{"cat": "Protéines", "p": "Poulet",
            "maxi":  {"price": 2.49, "unit": "$/lb", "note": "poulet entier frais"},
            "metro": {"price": 2.69, "unit": "$/lb"}}]}
```

- Clés d'épicerie: `maxi`, `iga`, `metro`, `provigo`, `superc`, `adonis`.
- Offre: `price` (obligatoire), `unit` (`$` par défaut, `$/lb`, `$/kg`), `regular` (prix régulier), `note`.
- L'historique relie les semaines par le nom du produit `p` (ou par `id` s'il est fourni): garder le même nom d'une semaine à l'autre.
- Le champ `best` des anciennes données est ignoré: le meilleur prix est recalculé selon les épiceries choisies.

Prix tirés des circulaires et des sites des épiceries, à valider en magasin. Projet personnel, non affilié aux épiceries.
