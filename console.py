"""Interface console de BiblioIT."""
from datetime import date
from depot_sqlite import DepotSQLite
from service import ServiceBibliotheque
from regles import ErreurBiblio

def afficher_livres(livres):
    if not livres:
        print("Aucun livre trouvé.")
        return
    print("\nCODE   TITRE                               AUTEUR                  ANNÉE  ÉTAT")
    print("-" * 90)
    for l in livres:
        etat = "Disponible" if l.disponible else "Emprunté"
        print(f"{l.code:<6} {l.titre[:34]:<35} {l.auteur[:22]:<23} {str(l.annee or '-'):<6} {etat}")

def menu():
    print("\n=== BiblioIT ===")
    print("1. Rechercher un livre")
    print("2. Emprunter")
    print("3. Rendre")
    print("4. Retards")
    print("0. Quitter")

def main():
    service = ServiceBibliotheque(DepotSQLite())
    service.initialiser_catalogue_demo()
    print("Bienvenue dans BiblioIT — gestion de la bibliothèque")
    while True:
        menu()
        choix = input("Votre choix : ").strip()
        try:
            if choix == "1":
                terme = input("Titre, auteur ou code (Entrée = tout) : ")
                afficher_livres(service.rechercher_livres(terme))
            elif choix == "2":
                code = input("Code du livre : ")
                matricule = input("Matricule : ")
                _, retour = service.emprunter(code, matricule)
                print(f"Emprunt enregistré. Retour prévu le {retour.strftime('%d/%m/%Y')}.")
            elif choix == "3":
                code = input("Code du livre : ")
                matricule = input("Matricule : ")
                service.retourner(code, matricule)
                print("Retour enregistré. Merci !")
            elif choix == "4":
                retards = service.lister_retards()
                if not retards:
                    print("Aucun retard.")
                else:
                    for emprunt, titre in retards:
                        print(f"{emprunt.code_livre} — {titre} | {emprunt.matricule} | "
                              f"retour prévu le {emprunt.date_retour_prevue:%d/%m/%Y}")
            elif choix == "0":
                print("Au revoir.")
                break
            else:
                print("Choix invalide.")
        except ErreurBiblio as exc:
            print(f"Impossible : {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir.")
            break

if __name__ == "__main__":
    main()
