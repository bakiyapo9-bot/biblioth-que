"""Règles métier et validations du projet BiblioIT."""
from datetime import date, timedelta

DUREE_EMPRUNT_JOURS = 14

class ErreurBiblio(Exception):
    """Erreur métier affichable à l'utilisateur."""

def normaliser_code(code: str) -> str:
    return (code or "").strip().upper()

def valider_matricule(matricule: str) -> str:
    matricule = (matricule or "").strip().upper()
    if len(matricule) < 4 or " " in matricule:
        raise ErreurBiblio("Matricule invalide.")
    return matricule

def valider_code_livre(code: str) -> str:
    code = normaliser_code(code)
    if not code:
        raise ErreurBiblio("Le code du livre est obligatoire.")
    return code

def date_retour_prevue(date_emprunt: date | None = None) -> date:
    """Un emprunt dure 14 jours à partir de la date d'emprunt."""
    return (date_emprunt or date.today()) + timedelta(days=DUREE_EMPRUNT_JOURS)

def est_en_retard(date_prevue: date, aujourd_hui: date | None = None) -> bool:
    return date_prevue < (aujourd_hui or date.today())
