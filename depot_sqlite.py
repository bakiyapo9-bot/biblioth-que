"""Accès à la base SQLite (aucune règle métier ici)."""
import sqlite3
from contextlib import closing
from datetime import date

from modeles import Emprunt, Livre

# Un livre est disponible s'il n'a aucun emprunt sans date de retour.
SELECT_LIVRES = """
    SELECT code, titre, auteur, annee,
           NOT EXISTS (SELECT 1 FROM emprunts
                       WHERE code_livre = code AND date_retour_effective IS NULL)
    FROM livres
"""


class DepotSQLite:
    def __init__(self, chemin: str = "bibliit.db"):
        self.chemin = chemin
        with closing(sqlite3.connect(chemin)) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS livres (
                    code TEXT PRIMARY KEY,
                    titre TEXT NOT NULL,
                    auteur TEXT NOT NULL,
                    annee INTEGER
                );
                CREATE TABLE IF NOT EXISTS emprunts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_livre TEXT NOT NULL REFERENCES livres(code),
                    matricule TEXT NOT NULL,
                    date_emprunt TEXT NOT NULL,
                    date_retour_prevue TEXT NOT NULL,
                    date_retour_effective TEXT
                );
            """)

    def _executer(self, sql: str, parametres: tuple = ()) -> list:
        """Exécute une requête, enregistre les modifications et renvoie les lignes."""
        with closing(sqlite3.connect(self.chemin)) as conn:
            with conn:  # commit automatique
                return conn.execute(sql, parametres).fetchall()

    def ajouter_livre(self, livre: Livre) -> None:
        self._executer("INSERT OR IGNORE INTO livres VALUES (?, ?, ?, ?)",
                       (livre.code, livre.titre, livre.auteur, livre.annee))

    def chercher_livres(self, mot_cle: str) -> list[Livre]:
        motif = f"%{mot_cle.strip()}%"
        lignes = self._executer(
            SELECT_LIVRES + " WHERE code LIKE ? OR titre LIKE ? OR auteur LIKE ? ORDER BY titre",
            (motif, motif, motif))
        return [Livre(c, t, a, an, bool(d)) for c, t, a, an, d in lignes]

    def obtenir_livre(self, code: str) -> Livre | None:
        lignes = self._executer(SELECT_LIVRES + " WHERE code = ?", (code,))
        return Livre(*lignes[0][:4], bool(lignes[0][4])) if lignes else None

    def creer_emprunt(self, code: str, matricule: str, debut: date, retour: date) -> None:
        self._executer(
            "INSERT INTO emprunts (code_livre, matricule, date_emprunt, date_retour_prevue)"
            " VALUES (?, ?, ?, ?)",
            (code, matricule, debut.isoformat(), retour.isoformat()))

    def terminer_emprunt(self, code: str, matricule: str, jour: date) -> bool:
        """Enregistre le retour. Renvoie False si aucun emprunt en cours n'existe."""
        lignes = self._executer(
            "UPDATE emprunts SET date_retour_effective = ?"
            " WHERE code_livre = ? AND matricule = ? AND date_retour_effective IS NULL"
            " RETURNING id",
            (jour.isoformat(), code, matricule))
        return bool(lignes)

    def lister_retards(self, aujourd_hui: date) -> list[Emprunt]:
        lignes = self._executer("""
            SELECT e.code_livre, l.titre, e.matricule, e.date_retour_prevue
            FROM emprunts e JOIN livres l ON l.code = e.code_livre
            WHERE e.date_retour_effective IS NULL AND e.date_retour_prevue < ?
            ORDER BY e.date_retour_prevue
        """, (aujourd_hui.isoformat(),))
        return [Emprunt(c, t, m, date.fromisoformat(d)) for c, t, m, d in lignes]
