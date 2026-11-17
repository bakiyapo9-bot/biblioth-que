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

## Exécuter les tests
```bash
python -m unittest discover -s tests -v
```

## Architecture
- `regles.py` : validations, durée d'emprunt et règle de retard.
- `modeles.py` : objets `Livre` et `Emprunt`.
- `depot_sqlite.py` : accès à la base SQLite.
- `service.py` : opérations métier.
- `console.py` : menu et interactions avec l'utilisateur.
- `tests/` : tests unitaires des règles et services.

## Répartition de travail suggérée
- A : `regles.py`
- B : `modeles.py`
- C : `depot_sqlite.py`
- D : `service.py`
- E : `console.py`
- Chaque membre ajoute ses tests et soumet une Pull Request relue par une autre personne.

## Règles retenues
La diapositive indique les fonctions principales, mais ne précise pas la durée d'un prêt ni les règles de validation. Pour rendre le projet exécutable, cette version retient une durée de 14 jours, un seul emprunt actif par livre et un retour associé au matricule de l'emprunteur. Ces paramètres peuvent être adaptés dans `regles.py`.
