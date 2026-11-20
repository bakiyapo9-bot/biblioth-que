from dataclasses import dataclass
from datetime import date


@dataclass
class Livre:
    code: str
    titre: str
    auteur: str
    annee: int
    disponible: bool = True


@dataclass
class Emprunt:
    code_livre: str
    titre: str
    matricule: str
    date_retour_prevue: date
