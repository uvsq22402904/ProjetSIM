Voici un fichier `README.md` bien structuré et formaté en Markdown à partir de votre texte :

---

# Simulation de Routeur avec Groupes de Serveurs

Ce projet implémente une **simulation à événements discrets** d'un système de routage avec plusieurs groupes de serveurs. L'objectif est d'analyser l'impact du nombre de groupes (`C`) sur les performances d'un système distribué sous différentes charges de travail (`λ`), en identifiant les configurations optimales qui **minimisent le temps de réponse moyen (`W`)** tout en maintenant un **taux de perte inférieur à 5%**.

---

## Description du Projet

Le projet simule un **routeur** recevant des requêtes et les distribuant vers des groupes de serveurs.
**Paramètres principaux :**

* `N_SERVEURS`: 12 serveurs au total
* `QUEUE_SIZE`: Capacité maximale de la file du routeur (100 requêtes)
* `C`: Nombre de groupes de serveurs (1, 2, 3, 6)
* `λ`: Taux d'arrivée des requêtes (de 0.1 à 6, pas de 0.35)
* `SIMULATION_TIME`: Durée de simulation (1000 unités de temps)

---

## Architecture des Groupes

| C | Répartition des serveurs |
| - | ------------------------ |
| 1 | 1 groupe de 12 serveurs  |
| 2 | 2 groupes de 6 serveurs  |
| 3 | 3 groupes de 4 serveurs  |
| 6 | 6 groupes de 2 serveurs  |

---

## Temps de Service

Le temps de traitement suit une **loi exponentielle**, dont le taux `μ` dépend de `C` :

| C | Taux (μ) | Moyenne du temps de service (1/μ) |
| - | -------- | --------------------------------- |
| 1 | 0.2      | 5.00 unités                       |
| 2 | 0.35     | 2.86 unités                       |
| 3 | 0.5      | 2.00 unités                       |
| 6 | 0.7      | 1.43 unités                       |

---

## Installation

1. **Créer un environnement virtuel** :

```bash
python -m venv envPRO
```

2. **Activer l'environnement** :

* **Windows** :

```bash
envPRO\Scripts\activate
```

* **Mac/Linux** :

```bash
source envPRO/bin/activate
```

3. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

### Dépendances

* `numpy` : Génération aléatoire, calculs numériques
* `matplotlib` : Visualisation
* `heapq` : File de priorité (standard)

---

## Utilisation

Lancer la simulation complète :

```bash
python Projet.py
```

---

## Structure du Code

### Fonctions & Classes Principales

* `exp_rnd(lmbda)` : Génère un nombre exponentiel de taux `lmbda`
* `class Requete` : Contient `time` (arrivée), `category` (groupe cible)
* `class Serveur` : Gère l’état `busy`, `end_time`
* `class Routeur` :

  * `queue` : File FIFO (max 100)
  * `servers` : Serveurs par groupe
  * `receive_request()`, `dispatch_to_server()`, `end_service()`, etc.
* `moyenne(data)` / `variance(data)` / `confidence_interval(data)`
* `simulate(C, lmbda)` : Retourne `W` et `loss_rate`
* `run_all_simulations()` : Exécute toutes les simulations
* `plot_response_time(results)` : Graphe `W` vs `λ`
* `plot_loss_rate(results, lambda_limits)`
* `find_optimal_C_for_lambda_1(results)`
* `find_optimal_C_for_all_lambdas(results, lambda_limits)`

---

## Analyse et Résultats

### Métriques

* **Temps de réponse moyen (W)** : `W = L / λ_eff`
* **Taux de perte** : Proportion de requêtes rejetées
* **Intervalle de confiance (95%)** : Moyenne ± marge

### Configuration optimale (résumé)

| λ      | C optimal | W (temps de réponse) |
| ------ | --------- | -------------------- |
| 0.10   | 6         | 2.37                 |
| 0.45   | 6         | 2.53                 |
| 0.80   | 3         | 2.98                 |
| 1.15   | 3         | 3.69                 |
| 1.50   | 2         | 4.16                 |
| 1.85   | 1         | 5.57                 |
| 2.20   | 1         | 9.28                 |
| 2.55   | 1         | 30.13                |
| ≥ 2.90 | Aucun     | Taux de perte > 5%   |

---

## Analyse Complémentaire

* **Faible charge (`λ < 0.80`)** : `C=6` est optimal
* **Charge moyenne (`0.80 ≤ λ < 1.50`)** : `C=3` ou `C=2`
* **Charge modérée à élevée (`λ ≥ 1.85`)** : `C=1` est préférable
* **Charge très élevée (`λ ≥ 2.90`)** : Aucune configuration ne satisfait le taux de perte

---

## Conclusion

* Le **choix optimal de `C` dépend de `λ`**.
* Plus `λ` est faible, plus un **parallélisme élevé (`C` élevé)** est bénéfique.
* Pour des charges plus lourdes, **moins de groupes mais plus de serveurs par groupe** deviennent préférables.
* Une **stratégie dynamique d’adaptation de `C`** permettrait d’optimiser la performance.

---

## Auteurs

* **Arris Yanis**
* **Benali Mohamed Amine**

---

## 📚 Références

* Théorie des files d'attente
* Simulation à événements discrets
* Loi exponentielle
* Loi de Little


