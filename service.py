"""Services applicatifs : orchestration des règles et du dépôt."""
import sqlite3
from datetime import date
from depot_sqlite import DepotSQLite
from modeles import Livre
from regles import (
    ErreurBiblio, normaliser_code, valider_code_livre, valider_matricule,
    date_retour_prevue
)

class ServiceBibliotheque:
    def __init__(self, depot: DepotSQLite):
        self.depot = depot

    def initialiser_catalogue_demo(self):
        """Ajoute quelques livres d'exemple sans écraser les données existantes."""
        exemples = [
            Livre("1004", "Allah n'est pas obligé", "Ahmadou Kourouma", 2000),
            Livre("L002", "Les Soleils des indépendances", "Ahmadou Kourouma", 1968),
            Livre("L003", "Une si longue lettre", "Mariama Bâ", 1979),
            Livre("L004", "L'Aventure ambiguë", "Cheikh Hamidou Kane", 1961),
        ]
        for livre in exemples:
            self.depot.ajouter_livre(livre)

    def rechercher_livres(self, terme: str = ""):
        return self.depot.chercher_livres(terme)

    def emprunter(self, code_livre: str, matricule: str, aujourd_hui: date | None = None):
        code = valider_code_livre(code_livre)
        matricule = valider_matricule(matricule)
        jour = aujourd_hui or date.today()
        livre = self.depot.obtenir_livre(code)
        if livre is None:
            raise ErreurBiblio(f"Aucun livre ne correspond au code {code}.")
        if not livre.disponible:
            raise ErreurBiblio(f"Le livre « {livre.titre} » est déjà emprunté.")
        retour = date_retour_prevue(jour)
        try:
            identifiant = self.depot.creer_emprunt(code, matricule, jour, retour)
        except sqlite3.IntegrityError:
            # Protection supplémentaire en cas de deux emprunts simultanés.
            raise ErreurBiblio("Ce livre vient d'être emprunté par un autre membre.")
        return identifiant, retour

    def retourner(self, code_livre: str, matricule: str, aujourd_hui: date | None = None):
        code = valider_code_livre(code_livre)
        matricule = valider_matricule(matricule)
        emprunt = self.depot.emprunt_actif(code, matricule)
        if emprunt is None:
            raise ErreurBiblio("Aucun emprunt actif trouvé pour ce livre et ce matricule.")
        self.depot.retourner_emprunt(emprunt.id, aujourd_hui or date.today())
        return emprunt

    def lister_retards(self, aujourd_hui: date | None = None):
        return self.depot.lister_retards(aujourd_hui or date.today())
