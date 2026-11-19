import unittest
from datetime import date

from regles import ErreurBiblio, date_retour_prevue, jours_de_retard, valider_code, valider_matricule


class TestRegles(unittest.TestCase):
    def test_date_retour_14_jours(self):
        self.assertEqual(date_retour_prevue(date(2026, 10, 1)), date(2026, 10, 15))

    def test_jours_de_retard(self):
        self.assertEqual(jours_de_retard(date(2026, 10, 15), date(2026, 10, 20)), 5)
        self.assertEqual(jours_de_retard(date(2026, 10, 15), date(2026, 10, 10)), 0)

    def test_matricule_mis_en_majuscules(self):
        self.assertEqual(valider_matricule(" e2026-001 "), "E2026-001")

    def test_matricule_invalide(self):
        with self.assertRaises(ErreurBiblio):
            valider_matricule(" ")

    def test_code_obligatoire(self):
        with self.assertRaises(ErreurBiblio):
            valider_code("  ")


if __name__ == "__main__":
    unittest.main()
