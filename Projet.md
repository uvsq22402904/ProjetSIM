### **Explication détaillée pour la simulation de la ferme de serveurs**  

Ton projet repose sur une **simulation à événements discrets (SED)** pour modéliser le fonctionnement d’une ferme de serveurs avec un **routeur** et plusieurs **groupes de serveurs spécialisés**. L’objectif est d’évaluer l’impact du paramètre \( C \) (nombre de groupes de serveurs) sur le **temps de réponse moyen** et le **taux de perte des requêtes**.  

---

## **1️⃣ Étapes de modélisation du système**  

### **1.1 Description des composants**  
- **Routeur**  
  - Il reçoit toutes les requêtes, identifie leur catégorie et les envoie aux serveurs spécialisés.  
  - Il a une file d’attente limitée à 100 requêtes.  
  - Il traite les requêtes en **FIFO** avec un temps de traitement \( T_r = \frac{C - 1}{C} \).  
  - Si la file est pleine, les requêtes en excès sont **perdues**.  

- **Serveurs**  
  - Chaque groupe de serveurs est spécialisé pour un **type de requête**.  
  - Il y a \( C \) groupes et chaque groupe a \( K = \frac{12}{C} \) serveurs.  
  - Une requête est immédiatement envoyée à un serveur libre de son groupe, sinon elle attend dans la file du routeur.  
  - Le temps de service suit une loi exponentielle de paramètre :  
    - \( \mu = \frac{4}{20} \) si \( C = 1 \)  
    - \( \mu = \frac{7}{20} \) si \( C = 2 \)  
    - \( \mu = \frac{10}{20} \) si \( C = 3 \)  
    - \( \mu = \frac{14}{20} \) si \( C = 6 \)  

---

### **1.2 Événements à gérer**  
Dans une **simulation à événements discrets (SED)**, le système évolue uniquement lorsqu’un événement se produit. Les principaux événements ici sont :  

1. **Arrivée d’une requête**  
   - Générée selon une loi exponentielle de paramètre \( \lambda \).  
   - Si la file d’attente du routeur n’est pas pleine, la requête est placée dans la file.  
   - Sinon, elle est perdue (on incrémente un compteur de pertes).  

2. **Traitement d’une requête par le routeur**  
   - Il sélectionne une requête en FIFO et la dirige vers un groupe de serveurs.  
   - S’il y a un serveur libre, la requête est immédiatement prise en charge.  
   - Sinon, elle reste dans la file d’attente du routeur.  
   - Temps de traitement fixé à \( T_r = \frac{C - 1}{C} \).  

3. **Fin de traitement d’une requête par un serveur**  
   - Le serveur devient libre et peut prendre une nouvelle requête s’il y en a dans la file.  

---

### **1.3 Objectifs des simulations**  
Pour chaque valeur de \( C \) et pour différentes valeurs de \( \lambda \), on doit :  
1. **Tracer le temps de réponse moyen** en fonction de \( \lambda \) (avec intervalles de confiance à 95%).  
2. **Tracer le taux de perte des requêtes** en fonction de \( \lambda \) et trouver la valeur limite où il dépasse 5%.  
3. **Déterminer la valeur optimale de \( C \)** pour minimiser le temps de réponse et respecter la contrainte du taux de perte.  

---

## **2️⃣ Implémentation de la simulation**  

### **2.1 Structure générale du code**  
On peut utiliser **une liste d’événements ordonnée** (un *heap* ou une liste triée) pour gérer la simulation efficacement.  

- **Définition des classes :**  
  - `Requête` : représente une requête avec un horodatage et une catégorie.  
  - `Routeur` : gère la file d’attente et dirige les requêtes vers les serveurs.  
  - `Serveur` : traite les requêtes et libère les ressources après un certain temps.  
  - `Simulation` : boucle principale qui exécute les événements dans l’ordre chronologique.  

- **Boucle principale de simulation :**  
  - Récupérer le prochain événement.  
  - Mettre à jour l’état du système (file d’attente, serveurs, etc.).  
  - Générer les nouveaux événements correspondants (ex : nouvelle arrivée de requête, fin de service).  

- **Collecte des statistiques :**  
  - Mesurer le **temps de réponse moyen**.  
  - Calculer le **taux de perte** et vérifier la limite des 5%.  
  - Générer les courbes demandées.  

---

### **2.2 Algorithmes clés**  

#### **Génération des requêtes (arrivées)**
On génère le temps entre deux arrivées avec une **loi exponentielle** de paramètre \( \lambda \) :
\[
T_{\text{arrivée}} = -\frac{\ln(U)}{\lambda}, \quad  U \sim \mathcal{U}(0,1)
\]

#### **Temps de traitement du routeur**
\[
T_r = \frac{C - 1}{C}
\]

#### **Temps de service des serveurs**
Les serveurs suivent une **loi exponentielle** avec \( \mu \) dépendant de \( C \) :
\[
T_{\text{service}} = -\frac{\ln(U)}{\mu}, \quad U \sim \mathcal{U}(0,1)
\]

#### **File d’attente FIFO dans le routeur**
On utilise une **file FIFO** avec une capacité de 100.  

#### **Planification des événements**
On maintient une **file triée d’événements** et on exécute toujours le prochain événement le plus proche dans le temps.

---

## **3️⃣ Résultats attendus et analyse**  

Après l’exécution de la simulation, on doit :  
✅ **Tracer le temps de réponse moyen en fonction de \( \lambda \) pour chaque \( C \).**  
✅ **Tracer le taux de perte en fonction de \( \lambda \).**  
✅ **Déterminer les valeurs optimales de \( C \) en fonction de \( \lambda \).**  
✅ **Analyser les résultats pour justifier le choix optimal de \( C \).**  


