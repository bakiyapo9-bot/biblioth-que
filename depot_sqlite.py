"""Couche de persistance SQLite : aucun traitement métier ici."""
import sqlite3
from datetime import date
from pathlib import Path
from modeles import Livre, Emprunt

class DepotSQLite:
    def __init__(self, chemin: str = "bibliit.db"):
        self.chemin = str(chemin)
        self._initialiser()

    def _connexion(self):
        conn = sqlite3.connect(self.chemin)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _initialiser(self):
        with self._connexion() as conn:
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
                CREATE UNIQUE INDEX IF NOT EXISTS un_emprunt_actif_par_livre
                ON emprunts(code_livre) WHERE date_retour_effective IS NULL;
            """)

    def ajouter_livre(self, livre: Livre):
        with self._connexion() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO livres(code,titre,auteur,annee) VALUES(?,?,?,?)",
                (livre.code, livre.titre, livre.auteur, livre.annee)
            )

    def chercher_livres(self, terme: str = "") -> list[Livre]:
        terme = f"%{terme.strip()}%"
        with self._connexion() as conn:
            rows = conn.execute("""
                SELECT l.*,
                       CASE WHEN e.id IS NULL THEN 1 ELSE 0 END AS disponible
                FROM livres l
                LEFT JOIN emprunts e
                  ON e.code_livre=l.code AND e.date_retour_effective IS NULL
                WHERE l.code LIKE ? COLLATE NOCASE
                   OR l.titre LIKE ? COLLATE NOCASE
                   OR l.auteur LIKE ? COLLATE NOCASE
                ORDER BY l.titre
            """, (terme, terme, terme)).fetchall()
        return [Livre(r["code"], r["titre"], r["auteur"], r["annee"], bool(r["disponible"])) for r in rows]

    def obtenir_livre(self, code: str):
        livres = self.chercher_livres(code)
        return next((l for l in livres if l.code.upper() == code.upper()), None)

    def creer_emprunt(self, code: str, matricule: str, debut: date, retour_prevu: date) -> int:
        with self._connexion() as conn:
            cur = conn.execute("""
                INSERT INTO emprunts(code_livre,matricule,date_emprunt,date_retour_prevue)
                VALUES(?,?,?,?)
            """, (code, matricule, debut.isoformat(), retour_prevu.isoformat()))
            return cur.lastrowid

    def emprunt_actif(self, code: str, matricule: str | None = None):
        sql = """SELECT * FROM emprunts
                 WHERE code_livre=? AND date_retour_effective IS NULL"""
        params = [code]
        if matricule:
            sql += " AND matricule=?"
            params.append(matricule)
        with self._connexion() as conn:
            row = conn.execute(sql, params).fetchone()
        return self._vers_emprunt(row) if row else None

    def retourner_emprunt(self, emprunt_id: int, jour: date):
        with self._connexion() as conn:
            conn.execute(
                "UPDATE emprunts SET date_retour_effective=? WHERE id=? AND date_retour_effective IS NULL",
                (jour.isoformat(), emprunt_id)
            )

    def lister_retards(self, aujourd_hui: date):
        with self._connexion() as conn:
            rows = conn.execute("""
                SELECT e.*, l.titre FROM emprunts e
                JOIN livres l ON l.code=e.code_livre
                WHERE e.date_retour_effective IS NULL AND e.date_retour_prevue < ?
                ORDER BY e.date_retour_prevue
            """, (aujourd_hui.isoformat(),)).fetchall()
        return [(self._vers_emprunt(r), r["titre"]) for r in rows]

    @staticmethod
    def _vers_emprunt(row):
        return Emprunt(
            row["id"], row["code_livre"], row["matricule"],
            date.fromisoformat(row["date_emprunt"]),
            date.fromisoformat(row["date_retour_prevue"]),
            date.fromisoformat(row["date_retour_effective"]) if row["date_retour_effective"] else None
        )
