from datetime import date

from catalogue import CATALOGUE
from depot_sqlite import DepotSQLite
from modeles import Emprunt, Livre
from regles import ErreurBiblio, date_retour_prevue, valider_code, valider_matricule


class ServiceBibliotheque:
    def __init__(self, depot: DepotSQLite):
        self.depot = depot
        for livre in CATALOGUE:
            depot.ajouter_livre(livre)

    def rechercher(self, mot_cle: str = "") -> list[Livre]:
        return self.depot.chercher_livres(mot_cle)

    def emprunter(self, code: str, matricule: str, jour: date | None = None) -> date:
        code, matricule = valider_code(code), valider_matricule(matricule)
        livre = self.depot.obtenir_livre(code)
        if livre is None:
            raise ErreurBiblio(f"Aucun livre ne correspond au code {code}.")
        if not livre.disponible:
            raise ErreurBiblio(f"Le livre « {livre.titre} » est déjà emprunté.")
        jour = jour or date.today()
        retour = date_retour_prevue(jour)
        self.depot.creer_emprunt(code, matricule, jour, retour)
        return retour

    def rendre(self, code: str, matricule: str, jour: date | None = None) -> None:
        code, matricule = valider_code(code), valider_matricule(matricule)
        if not self.depot.terminer_emprunt(code, matricule, jour or date.today()):
            raise ErreurBiblio("Aucun emprunt en cours pour ce livre et ce matricule.")

    def retards(self, aujourd_hui: date | None = None) -> list[Emprunt]:
        return self.depot.lister_retards(aujourd_hui or date.today())
