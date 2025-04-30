# Simulation de Routeur avec Groupes de Serveurs

Ce projet implémente une simulation à événements discrets d'un système de routage avec plusieurs groupes de serveurs. Il permet d'étudier l'impact du nombre de groupes (C) sur les performances d'un système distribué face à différentes charges de travail (λ), avec pour objectif d'identifier les configurations optimales qui minimisent le temps de réponse tout en maintenant un faible taux de perte de requêtes.

## Description du Projet

Le projet simule un routeur qui reçoit des requêtes et les dirige vers différents groupes de serveurs. Le système est caractérisé par :

- **N_SERVEURS** : Nombre total de serveurs (fixé à 12)
- **QUEUE_SIZE** : Taille maximale de la file d'attente du routeur (fixé à 100)
- **C** : Nombre de groupes de serveurs (varie parmi 1, 2, 3, 6)
- **λ** : Taux d'arrivée des requêtes (entre 0.1 et 5)

Chaque requête est assignée à un groupe spécifique en fonction de sa catégorie, et le routeur maintient une file d'attente FIFO pour gérer les requêtes entrantes.

### Modèle de distribution des serveurs

- Le système dispose toujours de 12 serveurs au total, répartis en C groupes
- Pour C=1 : Un seul groupe de 12 serveurs
- Pour C=2 : Deux groupes de 6 serveurs chacun
- Pour C=3 : Trois groupes de 4 serveurs chacun
- Pour C=6 : Six groupes de 2 serveurs chacun

### Temps de service

Les temps de service sont distribués exponentiellement avec des moyennes qui dépendent de la valeur de C :
- C=1 : moyenne de 4/20 unités de temps
- C=2 : moyenne de 7/20 unités de temps
- C=3 : moyenne de 10/20 unités de temps
- C=6 : moyenne de 14/20 unités de temps

Ce modèle reflète les compromis entre le parallélisme (plus de groupes) et l'efficacité de traitement (groupes plus grands).

## Installation et Configuration

### Créer un environnement virtuel
Avant d'exécuter le projet, créez un environnement virtuel pour isoler les dépendances :
```bash
python -m venv envPRO
```

### Activer l'environnement virtuel
- **Windows (cmd/PowerShell) :**
  ```powershell
  envPRO\Scripts\activate
  ```
- **Mac/Linux :**
  ```bash
  source envPRO/bin/activate
  ```

### Installer les dépendances
Une fois l'environnement activé, installez les dépendances requises :
```bash
pip install -r requirements.txt
```

Alternativement, vous pouvez cloner le dépôt :
```bash
git clone https://github.com/username/router-simulation.git
cd router-simulation
pip install -r requirements.txt
```

## Dépendances

- NumPy
- Matplotlib
- heapq (standard library)

## Usage

Une fois l'environnement configuré et les dépendances installées, lancez la simulation avec :

```bash
python Projet.py
```

Pour exécuter la simulation complète et générer tous les graphiques :

```python
python simulation.py
```

Pour effectuer des simulations spécifiques :

```python
# Importer le module
from simulation import simulate, confidence_interval

# Simuler avec C=3 et λ=1.5
W, loss_rate = simulate(C=3, lmbda=1.5)
print(f"Temps de réponse moyen: {W}")
print(f"Taux de perte: {loss_rate}")

# Exécuter plusieurs simulations pour obtenir un intervalle de confiance
W_values = [simulate(C=3, lmbda=1.5)[0] for _ in range(10)]
mean_W, margin = confidence_interval(W_values)
print(f"Temps de réponse moyen: {mean_W} ± {margin}")
```

## Description des Fonctions

### 1. `exp_rnd(lmbda)`
- **Description** : Génère une variable aléatoire suivant une loi exponentielle avec un paramètre donné `λ`.
- **Entrée** : 
  - `lmbda` : Taux d'arrivée ou de service.
- **Sortie** : Une valeur aléatoire suivant une loi exponentielle.

### 2. Classe `Requete`
- **Description** : Représente une requête dans le système.
- **Attributs** :
  - `time` : Temps d'arrivée de la requête.
  - `category` : Catégorie de la requête (détermine le groupe de serveurs à utiliser).

### 3. Classe `Serveur`
- **Description** : Représente un serveur dans le système.
- **Attributs** :
  - `busy` : Indique si le serveur est occupé (`True`) ou libre (`False`).
  - `end_time` : Temps auquel le serveur termine son traitement actuel.

### 4. Classe `Routeur`
- **Description** : Gère la file d'attente et la répartition des requêtes vers les serveurs.
- **Attributs** :
  - `queue` : File d'attente FIFO pour les requêtes.
  - `capacity` : Taille maximale de la file d'attente.
  - `C` : Nombre de groupes de serveurs.
  - `servers` : Dictionnaire contenant les serveurs répartis en groupes.
  - `loss_count` : Nombre de requêtes perdues (file pleine).
- **Méthodes** :
  - `receive_request(event_queue, current_time, request)` : Ajoute une requête à la file d'attente ou la rejette si la file est pleine.
  - `route_request(event_queue, current_time)` : Dirige une requête de la file d'attente vers un serveur libre.
  - `end_service(event_queue, current_time, server, group)` : Libère un serveur après la fin d'un traitement.

### 5. `moyenne(data)`
- **Description** : Calcule la moyenne d'une liste de données.
- **Entrée** : `data` (liste de valeurs numériques).
- **Sortie** : Moyenne des valeurs.

### 6. `variance(data)`
- **Description** : Calcule la variance d'une liste de données.
- **Entrée** : `data` (liste de valeurs numériques).
- **Sortie** : Variance des valeurs.

### 7. `confidence_interval(data)`
- **Description** : Calcule la moyenne et la marge d'erreur pour un intervalle de confiance à 95%.
- **Entrée** : `data` (liste de valeurs numériques).
- **Sortie** : 
  - Moyenne des valeurs.
  - Marge d'erreur pour un intervalle de confiance à 95%.

### 8. `simulate(C, lmbda)`
- **Description** : Simule le fonctionnement du système pour une configuration donnée.
- **Entrées** :
  - `C` : Nombre de groupes de serveurs.
  - `lmbda` : Taux d'arrivée des requêtes.
- **Sorties** :
  - `W` : Temps de réponse moyen (calculé avec la loi de Little).
  - `loss_rate` : Taux de perte des requêtes.

### 9. `plot_response_time()`
- **Description** : Trace un graphique du temps de réponse moyen (`W`) en fonction de `λ` pour différentes valeurs de `C`.
- **Fonctionnement** :
  - Simule le système pour chaque combinaison de `C` et `λ`.
  - Calcule les moyennes et les marges d'erreur.
  - Affiche un graphique avec des barres d'erreur.

### 10. `plot_loss_rate()`
- **Description** : Trace un graphique du taux de perte en fonction de `λ` pour différentes valeurs de `C`.
- **Fonctionnement** :
  - Simule le système pour chaque combinaison de `C` et `λ`.
  - Calcule les moyennes et les marges d'erreur.
  - Affiche un graphique avec des barres d'erreur.
  - Identifie la valeur limite de `λ` où le taux de perte dépasse 5%.

### 11. `find_optimal_C_for_lambda_1()`
- **Description** : Détermine la valeur optimale de `C` pour `λ = 1`.
- **Fonctionnement** :
  - Simule le système pour chaque valeur de `C`.
  - Compare les temps de réponse moyens (`W`) et les taux de perte.
  - Sélectionne le `C` qui minimise `W` tout en respectant un taux de perte ≤ 5%.

### 12. `find_optimal_C_for_all_lambdas()`
- **Description** : Détermine la valeur optimale de `C` pour chaque valeur de `λ`.
- **Sortie** : Dictionnaire contenant le `C optimal` et le temps de réponse moyen (`W`) pour chaque `λ`.
- **Fonctionnement** :
  - Simule le système pour chaque combinaison de `C` et `λ`.
  - Compare les résultats pour identifier le `C` optimal.

### 13. Appels principaux
- **`plot_response_time()`** : Trace le graphique du temps de réponse moyen.
- **`plot_loss_rate()`** : Trace le graphique du taux de perte.
- **`find_optimal_C_for_lambda_1()`** : Trouve le `C optimal` pour `λ = 1`.
- **`find_optimal_C_for_all_lambdas()`** : Trouve le `C optimal` pour toutes les valeurs de `λ`.
- **Affichage des résultats** : Résume les choix optimaux pour chaque `λ`.

## Architecture du Code

- **Classe Requete** : Représente une requête avec un temps d'arrivée et une catégorie
- **Classe Serveur** : Représente un serveur qui peut être occupé ou libre
- **Classe Routeur** : Gère la file d'attente et le routage des requêtes vers les groupes de serveurs
- **Fonctions de simulation** : Implémentent la logique de simulation à événements discrets
- **Fonctions d'analyse** : Calculent les métriques et produisent les visualisations

## Métriques et Analyse

### Temps de Réponse Moyen (W)

Le temps moyen qu'une requête passe dans le système (file d'attente + traitement). Calculé via la loi de Little : W = L/λ où L est le nombre moyen de requêtes dans le système et λ est le taux d'arrivée effectif.

La simulation utilise une approche de calcul pondéré dans le temps pour estimer L :
```python
# Calcul de L via somme pondérée
total_weighted_requests += nb_in_system * delta
L = total_weighted_requests / total_time
```

### Taux de Perte

La proportion de requêtes qui sont rejetées car la file d'attente est pleine. Une requête est perdue quand elle arrive et que la file d'attente du routeur a atteint sa capacité maximale (QUEUE_SIZE = 100).

### Intervalle de Confiance

Pour chaque point de données, la simulation effectue 10 exécutions indépendantes pour calculer un intervalle de confiance à 95%. Cela permet d'évaluer la fiabilité des résultats et de quantifier leur variabilité.

## Résultats

La simulation analyse comment le nombre de groupes (C) affecte les performances du système en fonction du taux d'arrivée (λ). Deux métriques principales sont évaluées :

### 1. Temps de réponse moyen (W)

Le graphique de temps de réponse montre comment W varie en fonction de λ pour chaque valeur de C. On observe que :
- Pour des valeurs faibles de λ, C=6 donne les meilleurs résultats
- À mesure que λ augmente, C=3 devient plus performant
- Les configurations avec moins de groupes (C=1, C=2) se dégradent plus rapidement sous charge élevée

### 2. Taux de perte des requêtes

Le graphique du taux de perte montre le pourcentage de requêtes rejetées en fonction de λ. Points notables :
- C=1 atteint un taux de perte de 5% dès λ ≈ 2.5
- C=2 atteint ce seuil à λ ≈ 3.6
- C=3 maintient un faible taux de perte jusqu'à λ ≈ 4.0
- C=6 présente un comportement similaire à C=2

### 3. Configuration optimale

Pour chaque valeur de λ, la configuration optimale est celle qui minimise W tout en maintenant un taux de perte inférieur à 5%. Les résultats montrent que :
- Pour λ < 2.55 : C=6 est optimal
- Pour 2.55 ≤ λ < 4.0 : C=3 est optimal
- Pour λ ≥ 4.0 : aucune configuration ne satisfait le critère de perte < 5%

Ces transitions illustrent l'équilibre entre la distribution de charge (favorisée par un C élevé) et l'efficacité des ressources (favorisée par un C plus faible).

## Analyse des Résultats

### Observations clés

1. **Pour les faibles charges (λ < 2.5)** : 
   - Une valeur élevée de C (C=6) est optimale
   - La division en plusieurs petits groupes permet une meilleure distribution des requêtes
   - Les temps de réponse sont stables, autour de 2.0-2.3 unités de temps

2. **Pour les charges moyennes (2.5 < λ < 4.0)** :
   - C=3 devient optimal, offrant un meilleur équilibre entre parallélisme et taille des groupes
   - Le temps de réponse augmente progressivement avec λ, mais reste acceptable

3. **Pour les charges élevées (λ > 4.0)** :
   - Aucune configuration ne maintient un taux de perte inférieur à 5%
   - Le système atteint sa capacité maximale

Cette analyse montre que le choix optimal de C dépend fortement du taux d'arrivée des requêtes, avec une transition claire de C=6 à C=3 lorsque la charge augmente.

## Conclusions

Cette étude démontre l'importance d'adapter la configuration du routeur en fonction de la charge du système :

1. **Pour les systèmes à faible charge (λ < 2.55)** : Une organisation avec plusieurs petits groupes de serveurs (C=6) offre les meilleures performances, avec des temps de réponse minimaux.

2. **Pour les systèmes à charge moyenne (2.55 ≤ λ < 4.0)** : Une configuration intermédiaire avec C=3 représente le meilleur compromis entre distribution de la charge et efficacité de traitement.

3. **Pour les systèmes à forte charge (λ ≥ 4.0)** : Aucune configuration ne peut maintenir un taux de perte acceptable sans augmenter la capacité du système (par exemple en ajoutant plus de serveurs ou en augmentant la taille de la file d'attente).

Ces résultats soulignent l'importance de dimensionner correctement les systèmes distribués et d'adapter leur architecture en fonction des conditions de charge prévues.


## Auteur

Arris Yanis
Benali Mohamed Amine

## Références

- Théorie des files d'attente
- Simulation à événements discrets
- Loi de Little