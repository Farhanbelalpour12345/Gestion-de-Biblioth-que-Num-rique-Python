import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.table import Table
import csv

FICHIER_DATA = 'bibliotheque.json'

def generer_id_unique(livres: List[Dict[str, Any]]) -> int:
    """Retourne un ID unique (1 + max existant)."""
    if not livres:
        return 1
    max_id = max((livre.get('id', 0) for livre in livres), default=0)
    return max_id + 1

def verifier_livre(titre: str, auteur: str, annee: int, prix: float, genre: str) -> None:
    """Lève ValueError si une validation échoue."""
    current_year = datetime.now().year
    erreurs = []

    if not isinstance(titre, str) or not titre.strip():
        erreurs.append("Le titre ne peut pas être vide.")
    if not isinstance(auteur, str) or not auteur.strip():
        erreurs.append("L'auteur ne peut pas être vide.")
    if not isinstance(genre, str) or not genre.strip():
        erreurs.append("Le genre ne peut pas être vide.")
    if not isinstance(annee, int) or not (1000 <= annee <= current_year):
        erreurs.append(f"L'année doit être un entier entre 1000 et {current_year}.")
    if not (isinstance(prix, (int, float)) and prix > 0):
        erreurs.append("Le prix doit être un nombre strictement positif.")

    if erreurs:
        raise ValueError("; ".join(erreurs))

# ------------------
# Fonctions demandées par le sujet (noms conservés)
# ------------------

def ajouter_livre(livres: List[Dict[str, Any]], titre: str, auteur: str, genre: str, annee: int, prix: float) -> Dict[str, Any]:
    """Ajoute un livre après validation et retourne le dictionnaire ajouté."""
    verifier_livre(titre, auteur, annee, prix, genre)
    nouvel_id = generer_id_unique(livres)
    livre = {
        'id': nouvel_id,
        'titre': titre.strip(),
        'auteur': auteur.strip(),
        'genre': genre.strip(),
        'annee_publication': annee,
        'prix': float(prix),
        'disponible': True,
        'note': 0,
        'historique': []
    }
    livres.append(livre)
    return livre

RICH_CONSOLE = Console()

def afficher_tous_les_livres(livres: List[Dict[str, Any]]) -> None:
    """Affiche la liste des livres sous forme de table (rich)."""
    if not livres:
        RICH_CONSOLE.print("📚 La bibliothèque est vide.", style="bold red")
        return
    table = Table(title="📚 Bibliothèque")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Titre", style="magenta")
    table.add_column("Auteur", style="green")
    table.add_column("Genre", style="yellow")
    table.add_column("Année", justify="center")
    table.add_column("Prix (€)", justify="right")
    table.add_column("Statut", style="red")
    table.add_column("Note", style="bright_yellow")

    for l in livres:
        statut = "✅ Disponible" if l.get('disponible', False) else "❌ Emprunté"
        titre = (l.get('titre')[:27] + '...') if len(l.get('titre','')) > 30 else l.get('titre')
        note = int(l.get('note', 0) or 0)
        etoiles = '⭐' * note + '☆' * (5 - note)
        table.add_row(str(l.get('id', '')), titre, l.get('auteur', ''), l.get('genre', ''),
                      str(l.get('annee_publication', '')), f"{l.get('prix', 0.0):.2f}", statut, etoiles)
    RICH_CONSOLE.print(table)

def rechercher_livre(livres: List[Dict[str, Any]], critere: str, valeur: str) -> List[Dict[str, Any]]:
    """Recherche case-insensitive par titre, auteur ou genre. Retourne la liste des correspondances."""
    critere = critere.lower()
    valeur = valeur.lower().strip()
    if critere not in ('titre', 'auteur', 'genre'):
        raise ValueError("Critère de recherche invalide; utiliser 'titre', 'auteur' ou 'genre'.")
    resultats = [l for l in livres if valeur in str(l.get(critere, '')).lower()]
    return resultats

def supprimer_livre(livres: List[Dict[str, Any]], id_livre: int) -> bool:
    """Supprime un livre par id. Retourne True si supprimé, False sinon."""
    for i, l in enumerate(livres):
        if l.get('id') == id_livre:
            del livres[i]
            return True
    return False

# ------------------
# Emprunts / Retours
# ------------------

def trouver_par_id_interne(livres: List[Dict[str, Any]], id_livre: int) -> Optional[Dict[str, Any]]:
    """Helper: cherche un livre par id."""
    for l in livres:
        if l.get('id') == id_livre:
            return l
    return None

def emprunter_livre(livres: List[Dict[str, Any]], id_livre: int) -> None:
    """Marque un livre comme emprunté si disponible, lève ValueError sinon."""
    livre = trouver_par_id_interne(livres, id_livre)
    if livre is None:
        raise ValueError(f"Aucun livre trouvé avec l'ID {id_livre}.")
    if not livre.get('disponible', True):
        raise ValueError("Le livre est déjà emprunté.")
    livre['disponible'] = False
    livre.setdefault('historique', []).append({'action': 'emprunt', 'date': datetime.now().strftime("%Y-%m-%d %H:%M")})

def retourner_livre(livres: List[Dict[str, Any]], id_livre: int) -> None:
    """Marque un livre comme disponible si il était emprunté, lève ValueError sinon."""
    livre = trouver_par_id_interne(livres, id_livre)
    if livre is None:
        raise ValueError(f"Aucun livre trouvé avec l'ID {id_livre}.")
    if livre.get('disponible', True):
        raise ValueError("Le livre est déjà disponible (non emprunté).")
    livre['disponible'] = True
    livre.setdefault('historique', []).append({'action': 'retour', 'date': datetime.now().strftime("%Y-%m-%d %H:%M")})

def filtrer_par_genre(livres: List[Dict[str, Any]], genre: str) -> List[Dict[str, Any]]:
    """Retourne les livres d'un genre donné (case-insensitive)."""
    g = genre.lower().strip()
    return [l for l in livres if l.get('genre', '').lower() == g]

# ------------------
# Statistiques / Rapport
# ------------------

def generer_rapport(livres: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calcule et affiche des statistiques; retourne aussi un dictionnaire avec les valeurs."""
    total = len(livres)
    disponibles = sum(1 for l in livres if l.get('disponible', False))
    empruntes = total - disponibles
    prix_total = sum(float(l.get('prix', 0.0)) for l in livres)

    # Genre le plus fréquent
    genre_counts = {}
    for l in livres:
        g = l.get('genre', 'Inconnu')
        genre_counts[g] = genre_counts.get(g, 0) + 1
    genre_populaire = max(genre_counts.items(), key=lambda x: x[1])[0] if genre_counts else None

    # Livres les plus et moins chers
    livres_trie_par_prix = sorted(livres, key=lambda x: x.get('prix', 0.0))
    moins_chers = livres_trie_par_prix[:3] if livres_trie_par_prix else []
    plus_chers = livres_trie_par_prix[-3:][::-1] if livres_trie_par_prix else []

    rapport = {
        'total': total,
        'disponibles': disponibles,
        'empruntes': empruntes,
        'prix_total': prix_total,
        'genre_populaire': genre_populaire,
        'moins_chers': moins_chers,
        'plus_chers': plus_chers
    }

    # Affichage convivial
    print("\n📊 Rapport de la bibliothèque :")
    print(f"- Nombre total de livres : {total}")
    print(f"- Disponible(s) : {disponibles} ✅")
    print(f"- Emprunté(s) : {empruntes} ❌")
    print(f"- Valeur totale (prix) : {prix_total:.2f} €")
    if genre_populaire:
        print(f"- Genre le plus représenté : {genre_populaire}")

    if plus_chers:
        print("\n📈 Livres les plus chers :")
        for l in plus_chers:
            print(f" - {l.get('titre')} ({l.get('prix'):.2f} €) — ID {l.get('id')}")
    if moins_chers:
        print("\n📉 Livres les moins chers :")
        for l in moins_chers:
            print(f" - {l.get('titre')} ({l.get('prix'):.2f} €) — ID {l.get('id')}")

    return rapport

# ------------------
# Persistance (JSON)
# ------------------

def charger_bibliotheque(filename: str = FICHIER_DATA) -> List[Dict[str, Any]]:
    """Charge la bibliothèque depuis un fichier JSON. Si le fichier n'existe pas, retourne une liste vide."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError('Format de fichier invalide : attendu une liste de livres.')
            return data
    except json.JSONDecodeError as e:
        raise ValueError(f'Fichier JSON corrompu ou format invalide : {e}')
    except Exception:
        raise

def sauvegarder_bibliotheque(livres: List[Dict[str, Any]], filename: str = FICHIER_DATA) -> None:
    """Sauvegarde la liste de livres dans le fichier JSON. Lève exception si échec."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(livres, f, ensure_ascii=False, indent=4)
    except TypeError as e:
        raise ValueError(f'Erreur de sérialisation JSON : {e}')
    except Exception:
        raise

# ------------------
# Fonctions utilitaires supplémentaires renommées (bonus)
# ------------------

def trier_catalogue(livres: List[Dict[str, Any]], cle: str = 'titre') -> List[Dict[str, Any]]:
    """Retourne une nouvelle liste triée par 'titre', 'auteur' ou 'prix'."""
    if cle not in ('titre', 'auteur', 'prix'):
        raise ValueError("Clé de tri invalide : 'titre', 'auteur' ou 'prix'.")
    if cle == 'prix':
        return sorted(livres, key=lambda x: x.get('prix', 0.0))
    return sorted(livres, key=lambda x: x.get(cle, '').lower())

def ajouter_note(livres: List[Dict[str, Any]], id_livre: int, note: int) -> None:
    """Attribue une note de 1 à 5 à un livre."""
    if note < 1 or note > 5:
        raise ValueError("La note doit être entre 1 et 5.")
    livre = trouver_par_id_interne(livres, id_livre)
    if not livre:
        raise ValueError(f"Aucun livre trouvé avec l'ID {id_livre}.")
    livre['note'] = int(note)

def afficher_journal(livres: List[Dict[str, Any]], id_livre: int) -> None:
    """Affiche l'historique (journal) d'un livre."""
    livre = trouver_par_id_interne(livres, id_livre)
    if not livre:
        print("❌ Aucun livre trouvé avec cet ID.")
        return
    hist = livre.get('historique', [])
    if not hist:
        print("📜 Aucune action enregistrée pour ce livre.")
        return
    print(f"\n📜 Historique pour '{livre['titre']}' :")
    for h in hist:
        action = "Emprunté" if h['action'] == 'emprunt' else "Retour"
        print(f" - {h['date']} : {action}")

def recherche_combinee(livres: List[Dict[str, Any]], titre: str = None, auteur: str = None, genre: str = None) -> List[Dict[str, Any]]:
    """Recherche par combinaison de critères (titre partiel, auteur partiel, genre exact)."""
    resultats = livres
    if titre:
        resultats = [l for l in resultats if titre.lower() in l.get('titre', '').lower()]
    if auteur:
        resultats = [l for l in resultats if auteur.lower() in l.get('auteur', '').lower()]
    if genre:
        resultats = [l for l in resultats if genre.lower() == l.get('genre', '').lower()]
    return resultats

def sauvegarder_csv(livres: List[Dict[str, Any]], filename: str = 'bibliotheque.csv') -> None:
    """Exporte la bibliothèque au format CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        champs = ['id','titre','auteur','genre','annee_publication','prix','disponible','note']
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        for l in livres:
            writer.writerow({k: l.get(k) for k in champs})
