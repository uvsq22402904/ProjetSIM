# 📌 **Simulation d'une Ferme de Serveurs**

## **1️⃣ Introduction**
Ce projet simule une **ferme de 12 serveurs** traitant des requêtes selon différents regroupements (`C = 1, 2, 3, 6`).  
L’objectif est de **trouver la meilleure configuration de `C`** pour **minimiser le temps de réponse moyen** tout en respectant une **limite de 5% de taux de perte**.

## Installation et Configuration

### 1️⃣ Créer un environnement virtuel
Avant d'exécuter le projet, créez un environnement virtuel pour isoler les dépendances :
```bash
python -m venv envPRO
```

### 2️⃣ Activer l’environnement virtuel
- **Windows (cmd/PowerShell) :**
  ```powershell
  envPRO\Scripts\activate
  ```
- **Mac/Linux :**
  ```bash
  source envPRO/bin/activate
  ```

### 3️⃣ Installer les dépendances
Une fois l’environnement activé, installez les dépendances requises :
```bash
pip install -r requirements.txt
```

---

## **3️⃣ Description du Code**

### **📌 Paramètres globaux**
- `N_SERVEURS = 12` → Nombre total de serveurs.  
- `QUEUE_SIZE = 100` → Taille maximale de la file d'attente du routeur.  
- `C_VALUES = [1, 2, 3, 6]` → Nombre de groupes de serveurs testés.  
- `LAMBDA_VALUES = np.linspace(0.1, 10, 15)` → Valeurs de `λ` testées.  
- `SIMULATION_TIME = 10000` → Durée totale de la simulation.  

---

### **📌 Modélisation du système**
- **`Requete`** : Représente une requête avec son **temps d’arrivée** et sa **catégorie**.  
- **`Serveur`** : Représente un serveur, avec un état (`occupé ou non`).  
- **`Routeur`** :
  - Gère une **file d’attente FIFO** de taille limitée (`100 requêtes max`).  
  - **Dirige les requêtes** vers des **serveurs spécialisés**.  
  - **Gère le taux de perte** si la file est pleine.

---

### **📌 Simulation et Gestion des Événements**
La simulation utilise une **file d’événements triée** (`heapq`) avec :  
1. **`arrival`** → Une requête arrive. Si la file **est pleine**, elle est **perdue**.  
2. **`route_request`** → Le routeur dirige la requête vers un serveur **disponible**.  
3. **`end_service`** → Un serveur termine son traitement et devient **libre**.  

Le **temps d’arrivée et de service** suit une loi **exponentielle** pour modéliser un **système aléatoire**.

---

### **📌 Collecte des Statistiques**
- 📊 **Temps de réponse moyen** (`response_times[C]`).  
- ❌ **Taux de perte** (`loss_rates[C]`).  
- 📉 **Intervalles de confiance à 95%** (`response_intervals[C]` et `loss_intervals[C]`).  

La simulation est **répétée 30 fois** (`N_RUNS = 30`) pour assurer **des résultats fiables**.

---

### **📌 Détermination des Valeurs Optimales**
1. 🔍 **Détection de la valeur limite de `λ`** où la perte dépasse **5%**.  
2. ✅ **Sélection automatique du `C optimal`** pour **chaque valeur de `λ`**.  
3. 📌 **Analyse spécifique pour `λ = 1`** pour expliquer le choix optimal.

---

### **📌 Affichage des Résultats**
Le programme **affiche** :
- ✅ **Le `C optimal` pour chaque valeur de `λ`**.  
- ✅ **La valeur limite de `λ` où la perte dépasse 5%**.  
- 📊 **Deux Graphiques** :
  1. **Temps de réponse moyen en fonction de `λ`** (avec barres d’erreur).  
  2. **Taux de perte en fonction de `λ`** (avec barres d’erreur).  

---

## **4️⃣ Résultats & Interprétation**
- 🟢 **Pour `λ` faible, `C = 1` ou `C = 2`** est optimal.  
- 🔴 **À partir de `λ ≈ 1.5`, `C = 6` devient préférable** pour mieux gérer la charge.  
- 🔎 **Aucun dépassement de 5% de perte** observé → On peut tester des valeurs de `λ` plus grandes.  

---

## **5️⃣ Conclusion**
- ✅ **Simulation réussie** pour **analyser les performances d’une ferme de serveurs**.  
- ✅ **Optimisation automatique du paramètre `C`** en fonction de `λ`.  
- ✅ **Graphiques et intervalles de confiance pour valider les résultats**.  

