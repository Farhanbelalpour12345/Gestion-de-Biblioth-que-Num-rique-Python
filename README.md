# 📚 Bibliothèque Numérique (Gestion de Livres en Python)

Ce projet est une application Python en mode console permettant de gérer une bibliothèque numérique.  
L'utilisateur peut ajouter, rechercher, emprunter, retourner, supprimer et noter des livres tout en conservant les données dans un fichier JSON.

---

## 📌 1. Description du Projet

Ce projet a été développé dans le but de simuler la gestion d'une bibliothèque.  
Il permet aux utilisateurs d'interagir avec une collection de livres, d'effectuer des actions telles que l'ajout, la recherche, l'emprunt et le retour, tout en offrant des fonctionnalités de filtrage, tri et génération de rapports.

Les données sont stockées dans un fichier `bibliotheque.json` afin d'assurer la persistance entre les sessions.

---

## 🚀 2. Installation et Exécution

### ✔️ Prérequis
- Python **3.8 ou supérieur**
- Aucun module externe requis (tout est basé sur les bibliothèques standard de Python)

### 📥 Installation

1. Télécharger ou cloner le projet :
```bash
git clone https://github.com/Farhanbelalpour12345/Gestion-de-Biblioth-que-Num-rique-Python
```

2. Accéder au dossier :
```bash
cd bibliotheque-numerique
```

3. Lancer l'application :
```bash
python main.py
```

---

## 🛠️ 3. Fonctionnalités Implémentées

| Fonction | Description |
|---------|------------|
| ➕ Ajouter un livre | Permet l’ajout d’un livre avec titre, auteur, année, genre et prix |
| 📖 Afficher tous les livres | Affiche la liste complète des livres |
| 🔍 Rechercher un livre | Recherche par titre ou auteur |
| 📥 Emprunter un livre | Marque un livre comme emprunté |
| 📤 Retourner un livre | Réinitialise l'état d'un livre emprunté |
| 🗑️ Supprimer un livre | Retire un livre définitivement |
| ⭐ Noter un livre | Ajoute une note utilisateur au livre |
| 📂 Filtrer par genre | Affiche les livres selon leur catégorie |
| 🔢 Trier les livres | Tri par prix, année ou titre |
| 📄 Générer un rapport | Produit un résumé de l’état de la bibliothèque |
| 💾 Sauvegarde automatique | Persistance des données dans `bibliotheque.json` |

---

## 📘 4. Exemple d'Utilisation

📌 **Ajouter un livre :**
```
Entrez le titre : Les Misérables
Entrez l'auteur : Victor Hugo
Entrez l'année : 1862
Entrez le genre : Roman
Entrez le prix : 12.99€
→ Livre ajouté avec succès !
```

📌 **Rechercher un livre :**
```
Entrez un mot-clé : Hugo
→ Résultat : Les Misérables - Victor Hugo (Disponible)
```

📌 **Emprunter :**
```
Entrez le titre du livre à emprunter : Les Misérables
→ Le livre a été emprunté avec succès.
```

---

## 📦 Structure du Projet


📁 Bibliothèque_Numérique
 ├── main.py
 ├── bibliotheque.py
 ├── bibliotheque.json  (généré automatiquement)
 └── README.md
```



## ✍️ Auteur

👨‍💻 Développé par *Mohammad Belalpour*

