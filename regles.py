from datetime import date, timedelta

DUREE_EMPRUNT = 14


class ErreurBiblio(Exception):
    pass


def valider_code(code: str) -> str:
    code = code.strip().upper()
    if not code:
        raise ErreurBiblio("Le code du livre est obligatoire.")
    return code


def valider_matricule(matricule: str) -> str:
    matricule = matricule.strip().upper()
    if len(matricule) < 4 or " " in matricule:
        raise ErreurBiblio("Matricule invalide.")
    return matricule


def date_retour_prevue(jour: date) -> date:
    return jour + timedelta(days=DUREE_EMPRUNT)


def jours_de_retard(date_prevue: date, aujourd_hui: date) -> int:
    return max(0, (aujourd_hui - date_prevue).days)
