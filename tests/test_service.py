import tempfile
import unittest
from pathlib import Path
from datetime import date
from depot_sqlite import DepotSQLite
from service import ServiceBibliotheque
from regles import ErreurBiblio

class TestService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.depot = DepotSQLite(str(Path(self.tmp.name) / "test.db"))
        self.service = ServiceBibliotheque(self.depot)
        self.service.initialiser_catalogue_demo()

    def tearDown(self):
        self.tmp.cleanup()

    def test_recherche(self):
        livres = self.service.rechercher_livres("Kourouma")
        self.assertEqual(len(livres), 2)

    def test_emprunt_puis_indisponibilite(self):
        _, retour = self.service.emprunter("L002", "E2026-001", date(2026, 10, 1))
        self.assertEqual(retour, date(2026, 10, 15))
        livre = self.depot.obtenir_livre("L002")
        self.assertFalse(livre.disponible)
        with self.assertRaises(ErreurBiblio):
            self.service.emprunter("L002", "E2026-002", date(2026, 10, 2))

    def test_retour(self):
        self.service.emprunter("L002", "E2026-001", date(2026, 10, 1))
        self.service.retourner("L002", "E2026-001", date(2026, 10, 10))
        self.assertTrue(self.depot.obtenir_livre("L002").disponible)

    def test_retards(self):
        self.service.emprunter("L002", "E2026-001", date(2026, 10, 1))
        retards = self.service.lister_retards(date(2026, 10, 20))
        self.assertEqual(len(retards), 1)
        self.assertEqual(retards[0][0].matricule, "E2026-001")

if __name__ == "__main__":
    unittest.main()
