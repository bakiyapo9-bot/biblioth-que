import unittest
from datetime import date
from regles import date_retour_prevue, est_en_retard, valider_matricule, ErreurBiblio

class TestRegles(unittest.TestCase):
    def test_date_retour_14_jours(self):
        self.assertEqual(date_retour_prevue(date(2026, 10, 1)), date(2026, 10, 15))

    def test_retard(self):
        self.assertTrue(est_en_retard(date(2026, 10, 15), date(2026, 10, 16)))
        self.assertFalse(est_en_retard(date(2026, 10, 15), date(2026, 10, 15)))

    def test_matricule_normalise(self):
        self.assertEqual(valider_matricule(" e2026-001 "), "E2026-001")

    def test_matricule_invalide(self):
        with self.assertRaises(ErreurBiblio):
            valider_matricule(" ")

if __name__ == "__main__":
    unittest.main()
