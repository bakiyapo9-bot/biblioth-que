# BiblioIIT — Gestion de la bibliothèque

Application Python avec une interface graphique CustomTkinter et une base SQLite.

## Fonctionnalités
1. Rechercher un livre (titre, auteur ou code)
2. Emprunter un livre (retour prévu sous 14 jours)
3. Rendre un livre
4. Voir les emprunts en retard

## Lancement
```bash
python -m pip install -r requirements.txt
python interfaces.py
```
La base `bibliit.db` est créée automatiquement avec un catalogue de 100 œuvres africaines (L001 à L100),
défini dans `catalogue.py`.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Organisation

| Module            | Rôle                                 | Branche / membre      |
|-------------------|--------------------------------------|-----------------------|
| `regles.py`       | Validations, durée d'emprunt, retard | `feature/regles` — A  |
| `catalogue.py`    | Les 100 livres de départ             | `feature/base` — C    |
| `modeles.py`      | Classes `Livre` et `Emprunt`         | `feature/modeles` — B |
| `depot_sqlite.py` | Accès à la base SQLite               | `feature/base` — C    |
| `service.py`      | Rechercher, emprunter, rendre        | `feature/service` — D |
| `interfaces.py`   | Interface graphique avec menu        | `feature/menu` — E    |
| `tests/`          | Tests unitaires                      | chacun ses tests      |
