"""Objets métier utilisés par BiblioIT."""
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Livre:
    code: str
    titre: str
    auteur: str
    annee: int | None = None
    disponible: bool = True

@dataclass(frozen=True)
class Emprunt:
    id: int
    code_livre: str
    matricule: str
    date_emprunt: date
    date_retour_prevue: date
    date_retour_effective: date | None = None

    @property
    def actif(self) -> bool:
        return self.date_retour_effective is None
