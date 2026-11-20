import tempfile
import unittest
from datetime import date
from pathlib import Path

from depot_sqlite import DepotSQLite
from regles import ErreurBiblio
from service import ServiceBibliotheque


class TestService(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        chemin = str(Path(self.dossier.name) / "test.db")
        self.service = ServiceBibliotheque(DepotSQLite(chemin))

    def tearDown(self):
        self.dossier.cleanup()

    def test_catalogue_de_100_livres(self):
        self.assertEqual(len(self.service.rechercher()), 100)

    def test_recherche_par_auteur(self):
        livres = self.service.rechercher("Kourouma")
        self.assertEqual(len(livres), 5)
        self.assertEqual(livres[0].titre, "Allah n'est pas obligé")

    def test_emprunt_puis_livre_deja_emprunte(self):
        retour = self.service.emprunter("L002", "E2026-001", date(2026, 10, 1))
        self.assertEqual(retour, date(2026, 10, 15))
        with self.assertRaises(ErreurBiblio) as erreur:
            self.service.emprunter("L002", "E2026-002", date(2026, 10, 1))
        self.assertIn("déjà emprunté", str(erreur.exception))

    def test_code_inconnu(self):
        with self.assertRaises(ErreurBiblio):
            self.service.emprunter("L999", "E2026-001")

    def test_rendre(self):
        self.service.emprunter("L002", "E2026-001")
        self.service.rendre("L002", "E2026-001")
        self.assertTrue(self.service.rechercher("L002")[0].disponible)
        with self.assertRaises(ErreurBiblio):
            self.service.rendre("L002", "E2026-001")

    def test_retards(self):
        self.service.emprunter("L002", "E2026-001", date(2026, 10, 1))
        self.assertEqual(self.service.retards(date(2026, 10, 10)), [])
        retards = self.service.retards(date(2026, 10, 20))
        self.assertEqual(retards[0].matricule, "E2026-001")


if __name__ == "__main__":
    unittest.main()
