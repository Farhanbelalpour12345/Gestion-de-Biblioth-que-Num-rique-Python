from bibliotheque import (
    ajouter_livre,
    afficher_tous_les_livres,
    rechercher_livre,
    emprunter_livre,
    retourner_livre,
    filtrer_par_genre,
    generer_rapport,
    supprimer_livre,
    charger_bibliotheque,
    sauvegarder_bibliotheque,
    trier_catalogue,
    ajouter_note,
    afficher_journal,
    recherche_combinee,
    sauvegarder_csv
)

def saisie_int_retry(prompt: str, allow_quit: bool = True) -> int:
    """Demande un entier en boucle ; renvoie l'entier ou lève ValueError si l'utilisateur annule ('q')."""
    while True:
        val = input(prompt).strip()
        if allow_quit and val.lower() == 'q':
            raise ValueError("Annulé par l'utilisateur.")
        try:
            return int(val)
        except ValueError:
            print("❌ Entrée invalide — entrez un nombre entier valide (ou 'q' pour annuler).")

def saisie_float_retry(prompt: str, allow_quit: bool = True) -> float:
    while True:
        val = input(prompt).strip()
        if allow_quit and val.lower() == 'q':
            raise ValueError("Annulé par l'utilisateur.")
        try:
            return float(val)
        except ValueError:
            print("❌ Entrée invalide — entrez un nombre (ex: 19.99) ou 'q' pour annuler.")

def saisie_texte_nonvide(prompt: str, allow_quit: bool = True) -> str:
    while True:
        val = input(prompt).strip()
        if allow_quit and val.lower() == 'q':
            raise ValueError("Annulé par l'utilisateur.")
        if val:
            return val
        print("❌ Le champ ne peut pas être vide (ou tapez 'q' pour annuler).")

if __name__ == '__main__':
    livres = []
    # Chargement initial
    try:
        livres = charger_bibliotheque()
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement du fichier : {e}")
        livres = []

    # Si vide, exemples initiaux
    if not livres:
        exemples = [
            ("1984", "George Orwell", "Dystopie", 1949, 12.99),
            ("Le Petit Prince", "Antoine de Saint-Exupéry", "Conte", 1943, 9.50),
            ("Harry Potter à l'école des Sorciers", "J.K. Rowling", "Fantasy", 1997, 19.99),
            ("Clean Code", "Robert C. Martin", "Informatique", 2008, 34.90),
            ("Sapiens", "Yuval Noah Harari", "Histoire", 2011, 24.00),
            ("Le Comte de Monte-Cristo", "Alexandre Dumas", "Aventure", 1844, 14.00),
            ("Algorithms", "Robert Sedgewick", "Informatique", 2011, 45.00),
            ("La Peste", "Albert Camus", "Roman", 1947, 11.00),
            ("Don Quichotte", "Miguel de Cervantes", "Roman", 1605, 16.50),
            ("Le Rouge et le Noir", "Stendhal", "Roman", 1830, 10.20),
        ]
        for t, a, g, y, p in exemples:
            try:
                ajouter_livre(livres, t, a, g, y, p)
            except ValueError:
                pass
        try:
            sauvegarder_bibliotheque(livres)
        except Exception:
            pass

    # Boucle principale
    while True:
        print("\n=== GESTION DE BIBLIOTHÈQUE ===")
        print("1. Ajouter un livre")
        print("2. Afficher tous les livres")
        print("3. Rechercher un livre")
        print("4. Emprunter un livre")
        print("5. Retourner un livre")
        print("6. Filtrer par genre")
        print("7. Afficher les statistiques")
        print("8. Supprimer un livre")
        print("9. Trier les livres")
        print("10. Noter un livre")
        print("11. Afficher historique un livre")
        print("12. Recherche avancée")
        print("13. Export CSV")
        print("0. Quitter")

        choix = input("Choisissez une option (0-13) : ").strip()

        try:
            if choix == '1':
                print("\n➕ Ajouter un livre (tapez 'q' à n'importe quel moment pour annuler)")
                try:
                    titre = saisie_texte_nonvide("Titre : ")
                    auteur = saisie_texte_nonvide("Auteur : ")
                    genre = saisie_texte_nonvide("Genre : ")
                    annee = saisie_int_retry("Année de publication (ex: 1997) : ")
                    prix = saisie_float_retry("Prix (ex: 19.99) : ")
                    livre = ajouter_livre(livres, titre, auteur, genre, annee, prix)
                    sauvegarder_bibliotheque(livres)
                    print(f"✅ Livre ajouté avec succès (ID {livre['id']})")
                except ValueError as e:
                    print(f"❌ Opération annulée / erreur : {e}")

            elif choix == '2':
                afficher_tous_les_livres(livres)

            elif choix == '3':
                # boucle de reprise si critere invalide
                while True:
                    try:
                        print("\n🔎 Recherche (critères: titre / auteur / genre). Tapez 'q' pour annuler.")
                        critere = input("Critère (titre / auteur / genre) : ").strip().lower()
                        if critere == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        valeur = input("Valeur à rechercher : ").strip()
                        res = rechercher_livre(livres, critere, valeur)
                        if not res:
                            print("🔍 Aucun résultat trouvé.")
                        else:
                            afficher_tous_les_livres(res)
                        break
                    except ValueError as e:
                        print(f"❌ {e} — réessayez ou tapez 'q' pour annuler.")
                        if str(e).lower().startswith('annulé'):
                            break

            elif choix == '4':
                # emprunter : boucle de retry pour ID
                while True:
                    try:
                        print("\n📥 Emprunter un livre (tapez 'q' pour annuler)")
                        id_l = input("ID du livre à emprunter : ").strip()
                        if id_l.lower() == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        id_l = int(id_l)
                        emprunter_livre(livres, id_l)
                        sauvegarder_bibliotheque(livres)
                        print("✅ Livre emprunté avec succès.")
                        break
                    except ValueError as e:
                        print(f"❌ {e} — réessayez ou tapez 'q' pour annuler.")
                        if str(e).lower().startswith('annulé'):
                            break

            elif choix == '5':
                while True:
                    try:
                        print("\n📤 Retourner un livre (tapez 'q' pour annuler)")
                        id_l = input("ID du livre à retourner : ").strip()
                        if id_l.lower() == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        id_l = int(id_l)
                        retourner_livre(livres, id_l)
                        sauvegarder_bibliotheque(livres)
                        print("✅ Livre retourné avec succès.")
                        break
                    except ValueError as e:
                        print(f"❌ {e} — réessayez ou tapez 'q' pour annuler.")
                        if str(e).lower().startswith('annulé'):
                            break

            elif choix == '6':
                print("\n📚 Filtrer par genre (tapez 'q' pour annuler)")
                genre = input("Genre à filtrer : ").strip()
                if genre.lower() == 'q':
                    print("Annulé.")
                else:
                    res = filtrer_par_genre(livres, genre)
                    if not res:
                        print("Aucun livre trouvé pour ce genre.")
                    else:
                        afficher_tous_les_livres(res)

            elif choix == '7':
                generer_rapport(livres)

            elif choix == '8':
                while True:
                    try:
                        print("\n🗑️ Supprimer un livre (tapez 'q' pour annuler)")
                        id_l = input("ID du livre à supprimer : ").strip()
                        if id_l.lower() == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        id_l = int(id_l)
                        conf = input("Voulez-vous vraiment supprimer ce livre ? (o/N) : ").strip().lower()
                        if conf == 'o':
                            ok = supprimer_livre(livres, id_l)
                            if ok:
                                sauvegarder_bibliotheque(livres)
                                print("✅ Livre supprimé.")
                            else:
                                print("❌ Aucun livre trouvé avec cet ID.")
                        else:
                            print("Annulé.")
                        break
                    except ValueError as e:
                        print(f"❌ {e} — réessayez ou tapez 'q' pour annuler.")
                        if str(e).lower().startswith('annulé'):
                            break

            elif choix == '9':
                print("\n🔀 Trier les livres")
                cle = input("Par quel critère trier ? (titre / auteur / prix) : ").strip().lower()
                try:
                    livres_tries = trier_catalogue(livres, cle)
                    afficher_tous_les_livres(livres_tries)
                except Exception as e:
                    print(f"❌ {e}")

            elif choix == '10':
                while True:
                    try:
                        print("\n⭐ Noter un livre (1-5). Tapez 'q' pour annuler")
                        id_l = input("ID du livre à noter : ").strip()
                        if id_l.lower() == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        id_l = int(id_l)
                        note = input("Note (1-5) : ").strip()
                        if note.lower() == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        note = int(note)
                        ajouter_note(livres, id_l, note)
                        sauvegarder_bibliotheque(livres)
                        print("✅ Livre noté avec succès.")
                        break
                    except ValueError as e:
                        print(f"❌ {e} — réessayez ou tapez 'q' pour annuler.")
                        if str(e).lower().startswith('annulé'):
                            break

            elif choix == '11':
                while True:
                    try:
                        print("\n📜 Afficher historique (tapez 'q' pour annuler)")
                        id_l = input("ID du livre pour afficher l'historique : ").strip()
                        if id_l.lower() == 'q':
                            raise ValueError("Annulé par l'utilisateur.")
                        id_l = int(id_l)
                        afficher_journal(livres, id_l)
                        break
                    except ValueError as e:
                        print(f"❌ {e} — réessayez ou tapez 'q' pour annuler.")
                        if str(e).lower().startswith('annulé'):
                            break

            elif choix == '12':
                print("\n🔎 Recherche avancée (laisser vide pour ignorer un champ)")
                titre = input("Titre (laisser vide si non) : ").strip() or None
                auteur = input("Auteur (laisser vide si non) : ").strip() or None
                genre = input("Genre (laisser vide si non) : ").strip() or None
                res = recherche_combinee(livres, titre, auteur, genre)
                if not res:
                    print("🔍 Aucun résultat trouvé.")
                else:
                    afficher_tous_les_livres(res)

            elif choix == '13':
                try:
                    sauvegarder_csv(livres)
                    print("✅ Export CSV réalisé avec succès sous 'bibliotheque.csv'.")
                except Exception as e:
                    print(f"❌ Erreur lors de l'export CSV : {e}")

            elif choix == '0':
                # sauvegarde et sortie propre
                print("Au revoir 👋 — sauvegarde en cours...")
                try:
                    sauvegarder_bibliotheque(livres)
                except Exception as e:
                    print(f"⚠️ Erreur lors de la sauvegarde : {e}")
                print("Fermeture terminée.")
                break  # quitte la boucle principale

            else:
                print("Option invalide — choisissez un nombre entre 0 et 13.")

        except Exception as e:
            # Attrape les erreurs inattendues sans renvoyer immédiatement au menu :
            print(f"Erreur inattendue : {e}")
            print("Retour au menu principal.")
