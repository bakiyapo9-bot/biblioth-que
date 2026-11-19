"""Interface graphique de BiblioIIT (CustomTkinter).

Lancement : python interfaces.py
"""
from datetime import date

import customtkinter as ctk

from depot_sqlite import DepotSQLite
from regles import ErreurBiblio, jours_de_retard
from service import ServiceBibliotheque

# Couleurs
BLANC = "#ffffff"
MENU = "#fff1e0"  # blanc orangé
ORANGE = "#f07c1b"
ORANGE_FONCE = "#d0650c"
ORANGE_CLAIR = "#ffe0bf"
LIGNE = "#fff8f0"
TEXTE = "#2b2b2b"
GRIS = "#707070"
VERT = "#2e7d32"
ROUGE = "#c62828"

MENU_ENTREES = [
    ("recherche", "1.  Rechercher un livre"),
    ("emprunt", "2.  Emprunter"),
    ("retour", "3.  Rendre"),
    ("retards", "4.  Retards"),
]


class Application(ctk.CTk):
    def __init__(self, service: ServiceBibliotheque):
        super().__init__(fg_color=BLANC)
        self.service = service
        self.title("BiblioIIT — Gestion de la bibliothèque")
        self.geometry("1000x620")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.creer_menu()
        self.pages = {
            "recherche": self.page_recherche(),
            "emprunt": self.page_formulaire("Emprunter", self.emprunter),
            "retour": self.page_formulaire("Rendre", self.rendre),
            "retards": self.page_retards(),
        }
        self.afficher("recherche")

    # ---------- Menu latéral ----------
    def creer_menu(self):
        menu = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=MENU)
        menu.grid(row=0, column=0, sticky="ns")
        menu.pack_propagate(False)
        ctk.CTkLabel(menu, text="BiblioIIT", font=("", 28, "bold"),
                     text_color=ORANGE).pack(anchor="w", padx=24, pady=(30, 0))
        ctk.CTkLabel(menu, text="Gestion de la bibliothèque",
                     text_color=GRIS).pack(anchor="w", padx=24, pady=(0, 30))

        self.boutons = {}
        for nom, texte in MENU_ENTREES:
            bouton = ctk.CTkButton(menu, text=texte, anchor="w", height=42, font=("", 15),
                                   fg_color="transparent", hover_color=ORANGE_CLAIR,
                                   text_color=TEXTE, command=lambda n=nom: self.afficher(n))
            bouton.pack(fill="x", padx=14, pady=3)
            self.boutons[nom] = bouton

        ctk.CTkButton(menu, text="0.  Quitter", anchor="w", height=42, font=("", 15),
                      fg_color="transparent", hover_color=ORANGE_CLAIR, text_color=ROUGE,
                      command=self.destroy).pack(side="bottom", fill="x", padx=14, pady=20)

    def afficher(self, nom: str):
        """Affiche la page choisie et met son bouton en surbrillance."""
        for cle, page in self.pages.items():
            page.grid_remove()
            self.boutons[cle].configure(fg_color="transparent", text_color=TEXTE)
        self.pages[nom].grid(row=0, column=1, sticky="nsew", padx=40, pady=30)
        self.boutons[nom].configure(fg_color=ORANGE, text_color=BLANC)
        if nom == "recherche":
            self.afficher_livres()
        elif nom == "retards":
            self.afficher_retards()

    # ---------- Outils communs ----------
    def nouvelle_page(self, titre: str) -> ctk.CTkFrame:
        page = ctk.CTkFrame(self, fg_color=BLANC)
        ctk.CTkLabel(page, text=titre, font=("", 26, "bold"),
                     text_color=TEXTE).pack(anchor="w", pady=(0, 20))
        return page

    def champ(self, parent, exemple: str) -> ctk.CTkEntry:
        entree = ctk.CTkEntry(parent, placeholder_text=exemple, width=420, height=40,
                              border_color=ORANGE_CLAIR, fg_color=BLANC, text_color=TEXTE)
        entree.pack(anchor="w", pady=6)
        return entree

    def bouton(self, parent, texte: str, commande) -> ctk.CTkButton:
        return ctk.CTkButton(parent, text=texte, command=commande, height=40, width=160,
                             fg_color=ORANGE, hover_color=ORANGE_FONCE, text_color=BLANC,
                             font=("", 14, "bold"))

    def remplir(self, liste, lignes: list, message_vide: str):
        """Affiche des lignes (texte, état, couleur de l'état) dans une liste."""
        for widget in liste.winfo_children():
            widget.destroy()
        if not lignes:
            ctk.CTkLabel(liste, text=message_vide, text_color=GRIS).pack(pady=20)
        for texte, etat, couleur in lignes:
            ligne = ctk.CTkFrame(liste, fg_color=LIGNE, corner_radius=8)
            ligne.pack(fill="x", pady=4)
            ctk.CTkLabel(ligne, text=texte, text_color=TEXTE, font=("", 14),
                         anchor="w").pack(side="left", padx=14, pady=10)
            ctk.CTkLabel(ligne, text=etat, text_color=couleur,
                         font=("", 13, "bold")).pack(side="right", padx=14)

    # ---------- Page 1 : recherche ----------
    def page_recherche(self) -> ctk.CTkFrame:
        page = self.nouvelle_page("Rechercher un livre")
        barre = ctk.CTkFrame(page, fg_color=BLANC)
        barre.pack(fill="x")
        self.mot_cle = ctk.CTkEntry(barre, placeholder_text="Mot-clé : titre, auteur ou code",
                                    height=40, border_color=ORANGE_CLAIR, fg_color=BLANC,
                                    text_color=TEXTE)
        self.mot_cle.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.mot_cle.bind("<Return>", lambda _: self.afficher_livres())
        self.bouton(barre, "Rechercher", self.afficher_livres).pack(side="left")
        self.liste_livres = ctk.CTkScrollableFrame(page, fg_color=BLANC)
        self.liste_livres.pack(fill="both", expand=True, pady=(15, 0))
        return page

    def afficher_livres(self):
        lignes = []
        for livre in self.service.rechercher(self.mot_cle.get()):
            etat, couleur = ("Disponible", VERT) if livre.disponible else ("Emprunté", ROUGE)
            texte = f"{livre.code}    {livre.titre} — {livre.auteur} ({livre.annee})"
            lignes.append((texte, etat, couleur))
        self.remplir(self.liste_livres, lignes, "Aucun livre trouvé.")

    # ---------- Pages 2 et 3 : emprunter / rendre ----------
    def page_formulaire(self, titre: str, action) -> ctk.CTkFrame:
        page = self.nouvelle_page(titre)
        code = self.champ(page, "Code du livre (ex. L002)")
        matricule = self.champ(page, "Matricule (ex. E2026-001)")
        message = ctk.CTkLabel(page, text="", font=("", 14, "bold"), wraplength=600,
                               justify="left")

        def valider():
            try:
                message.configure(text=action(code.get(), matricule.get()), text_color=VERT)
            except ErreurBiblio as erreur:
                message.configure(text=f"Impossible : {erreur}", text_color=ROUGE)

        self.bouton(page, "Valider", valider).pack(anchor="w", pady=15)
        message.pack(anchor="w")
        return page

    def emprunter(self, code: str, matricule: str) -> str:
        retour = self.service.emprunter(code, matricule)
        return f"Emprunt enregistré. Retour prévu le {retour:%d/%m/%Y}."

    def rendre(self, code: str, matricule: str) -> str:
        self.service.rendre(code, matricule)
        return "Retour enregistré. Merci !"

    # ---------- Page 4 : retards ----------
    def page_retards(self) -> ctk.CTkFrame:
        page = self.nouvelle_page("Retards")
        self.liste_retards = ctk.CTkScrollableFrame(page, fg_color=BLANC)
        self.liste_retards.pack(fill="both", expand=True)
        return page

    def afficher_retards(self):
        lignes = []
        for e in self.service.retards():
            texte = (f"{e.code_livre}    {e.titre} — {e.matricule}, "
                     f"retour prévu le {e.date_retour_prevue:%d/%m/%Y}")
            jours = jours_de_retard(e.date_retour_prevue, date.today())
            lignes.append((texte, f"{jours} jour(s) de retard", ROUGE))
        self.remplir(self.liste_retards, lignes, "Aucun retard.")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    Application(ServiceBibliotheque(DepotSQLite())).mainloop()
