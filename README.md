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

## Arborescence

```
biblioth-que/
├── .github/
│   └── workflows/
│       └── tests.yml
├── tests/
│   ├── test_regles.py
│   └── test_service.py
├── .gitignore
├── catalogue.py
├── depot_sqlite.py
├── interfaces.py
├── modeles.py
├── regles.py
├── service.py
├── requirements.txt
└── README.md
```
