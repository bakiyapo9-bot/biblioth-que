# BiblioIT — Gestion de bibliothèque

Application console Python en équipe, organisée en cinq modules.

## Fonctionnalités
- Rechercher les livres par code, titre ou auteur.
- Enregistrer un emprunt avec matricule.
- Calculer automatiquement la date de retour prévue (14 jours).
- Enregistrer le retour d'un livre.
- Afficher les emprunts en retard.
- Stocker les données durablement dans SQLite.

## Prérequis
Python 3.10 ou supérieur. Aucune dépendance externe : SQLite est inclus dans Python.

## Lancer l'application
Depuis le dossier du projet :

```bash
python console.py
```

La base `bibliit.db` est créée automatiquement au premier lancement. Un petit catalogue de démonstration est ajouté sans écraser les données déjà présentes.



## Architecture
- `regles.py` : validations, durée d'emprunt et règle de retard.
- `modeles.py` : objets `Livre` et `Emprunt`.
- `depot_sqlite.py` : accès à la base SQLite.
- `service.py` : opérations métier.
- `console.py` : menu et interactions avec l'utilisateur.
- `tests/` : tests unitaires des règles et services.


