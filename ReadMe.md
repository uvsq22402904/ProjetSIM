Simulation de Routeur avec Groupes de Serveurs
Ce projet implémente une simulation à événements discrets d'un système de routage avec plusieurs groupes de serveurs. Il analyse l'impact du nombre de groupes (C) sur les performances d'un système distribué sous différentes charges de travail (λ), en cherchant à identifier les configurations optimales qui minimisent le temps de réponse tout en maintenant un taux de perte de requêtes inférieur à 5%.
Description du Projet
Le projet simule un routeur recevant des requêtes et les distribuant vers des groupes de serveurs. Les paramètres clés sont :

N_SERVEURS : 12 serveurs au total.
QUEUE_SIZE : Capacité maximale de la file d'attente du routeur (100 requêtes).
C : Nombre de groupes de serveurs (1, 2, 3, 6).
λ : Taux d'arrivée des requêtes (de 0.1 à 6, par pas de 0.35).
SIMULATION_TIME : Durée de chaque simulation (1000 unités de temps).

Chaque requête est assignée à un groupe selon sa catégorie, avec une file d'attente FIFO au niveau du routeur et des files d'attente par groupe pour les serveurs.
Modèle de Distribution des Serveurs

C=1 : 1 groupe de 12 serveurs.
C=2 : 2 groupes de 6 serveurs.
C=3 : 3 groupes de 4 serveurs.
C=6 : 6 groupes de 2 serveurs.

Temps de Service
Les temps de service suivent une loi exponentielle avec des taux dépendant de C. Le taux (noté μ) détermine la rapidité de traitement des requêtes, et la moyenne du temps de service est calculée comme 1/μ (en unités de temps). Voici les taux et leurs moyennes correspondantes :

C=1 : Taux = 4/20 = 0.2 → Moyenne = 1 / 0.2 = 5 unités de temps.
C=2 : Taux = 7/20 = 0.35 → Moyenne = 1 / 0.35 ≈ 2.86 unités de temps.
C=3 : Taux = 10/20 = 0.5 → Moyenne = 1 / 0.5 = 2 unités de temps.
C=6 : Taux = 14/20 = 0.7 → Moyenne = 1 / 0.7 ≈ 1.43 unités de temps.

Ces moyennes indiquent le temps moyen qu'un serveur met pour traiter une requête dans chaque configuration. Un taux plus élevé (donc une moyenne plus faible) reflète un traitement plus rapide, ce qui est cohérent avec un plus grand nombre de groupes (C élevé) permettant une meilleure distribution des requêtes, bien que chaque groupe ait moins de serveurs.
Installation et Configuration
Créer un environnement virtuel
python -m venv envPRO

Activer l'environnement virtuel

Windows :envPRO\Scripts\activate


Mac/Linux :source envPRO/bin/activate



Installer les dépendances
Installez les dépendances listées dans requirements.txt :
pip install -r requirements.txt

Ou, cloner le dépôt :
git clone https://github.com/username/router-simulation.git
cd router-simulation
pip install -r requirements.txt

Dépendances
Les dépendances sont spécifiées dans le fichier requirements.txt et incluent :

NumPy : Génération de nombres aléatoires et calculs.
Matplotlib : Visualisation des résultats.
heapq : Gestion de la file d'événements (bibliothèque standard).

Usage
Exécutez la simulation complète pour générer les graphiques et résultats :
python simulation.py

Pour une simulation spécifique :
from simulation import simulate, confidence_interval

# Simuler avec C=3, λ=1.5
W, loss_rate = simulate(C=3, lmbda=1.5)
print(f"Temps de réponse moyen: {W:.2f}")
print(f"Taux de perte: {loss_rate:.2%}")

# Intervalle de confiance
W_values = [simulate(C=3, lmbda=1.5)[0] for _ in range(10)]
mean_W, margin = confidence_interval(W_values)
print(f"Temps de réponse moyen: {mean_W:.2f} ± {margin:.2f}")

Description des Fonctions
1. exp_rnd(lmbda)
Génère une variable aléatoire exponentielle avec taux lmbda.
2. Classe Requete
Représente une requête avec :

time : Temps d'arrivée.
category : Groupe de serveurs cible.

3. Classe Serveur
Représente un serveur avec :

busy : État (occupé/libre).
end_time : Fin du traitement en cours.

4. Classe Routeur
Gère la file d'attente et le routage avec :

C : Nombre de groupes.
queue : File FIFO (capacité 100).
servers : Dictionnaire des serveurs par groupe.
waiting : Files d'attente par groupe.
loss_count : Requêtes perdues.
response_times : Temps de réponse des requêtes.
Méthodes :
receive_request : Accepte ou rejette une requête.
start_routing/end_routing : Gère le routage.
dispatch_to_server : Assigne une requête à un serveur.
end_service : Termine un service et traite les requêtes en attente.



5. moyenne(data)
Calcule la moyenne d'une liste.
6. variance(data)
Calcule la variance d'une liste.
7. confidence_interval(data)
Calcule la moyenne et la marge d'erreur (intervalle de confiance à 95%).
8. simulate(C, lmbda)
Simule le système pour un C et λ donnés, renvoyant :

W : Temps de réponse moyen.
loss_rate : Taux de perte.

9. run_all_simulations()
Exécute les simulations pour tous les C et λ, renvoyant :

results : Métriques (W, taux de perte, marges).
lambda_limits : Valeurs de λ où le taux de perte dépasse 5%.

10. plot_response_time(results)
Trace le temps de réponse moyen (W) vs λ pour chaque C, avec barres d'erreur.
11. plot_loss_rate(results, lambda_limits)
Trace le taux de perte vs λ pour chaque C, avec barres d'erreur, et affiche les limites de λ.
12. find_optimal_C_for_lambda_1(results)
Identifie le C optimal pour λ=1 (minimise W, taux de perte ≤ 5%).
13. find_optimal_C_for_all_lambdas(results, lambda_limits)
Détermine le C optimal pour chaque λ, avec résumé des résultats.
Architecture du Code

Requete : Structure une requête.
Serveur : Gère l'état d'un serveur.
Routeur : Orchestre le routage et la gestion des files.
Simulation : Logique à événements discrets.
Analyse : Calcul des métriques et visualisation.

Métriques et Analyse
Temps de Réponse Moyen (W)
Temps total passé par une requête dans le système (file + service). Calculé comme la moyenne des temps de réponse enregistrés.
Taux de Perte
Proportion de requêtes rejetées (file pleine ou file de groupe saturée).
Intervalle de Confiance
10 exécutions par configuration pour calculer des intervalles de confiance à 95%, assurant la robustesse des résultats.
Résultats
1. Temps de Réponse Moyen

Faibles λ : C=6 minimise W grâce au parallélisme.
Moyennes λ : C=3 devient optimal, équilibrant parallélisme et efficacité.
Hautes λ : W augmente rapidement pour tous les C.

2. Taux de Perte

C=1 : Perte > 5% dès λ ≈ 2.5.
C=2 : Perte > 5% à λ ≈ 3.6.
C=3 : Perte > 5% à λ ≈ 4.0.
C=6 : Perte > 5% à λ ≈ 3.6.

3. Configuration Optimale

λ < 2.55 : C=6 (meilleur parallélisme).
2.55 ≤ λ < 4.0 : C=3 (équilibre efficacité/parallélisme).
λ ≥ 4.0 : Aucun C ne maintient un taux de perte < 5%.

Analyse des Résultats

Faibles charges : C=6 excelle grâce à une distribution fine des requêtes.
Charges moyennes : C=3 optimise l'efficacité des serveurs.
Charges élevées : Le système sature, nécessitant une capacité accrue.

Conclusions
Le choix de C dépend fortement de λ. Une configuration dynamique ajustant C en fonction de la charge pourrait optimiser les performances. La simulation souligne l'importance de l'équilibre entre parallélisme et efficacité dans les systèmes distribués.
Auteurs

Arris Yanis
Benali Mohamed Amine

Références

Théorie des files d'attente
Simulation à événements discrets
Loi exponentielle

