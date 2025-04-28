import heapq
import numpy as np
import matplotlib.pyplot as plt
# Paramètres globaux
N_SERVEURS = 12
QUEUE_SIZE = 100
C_VALUES = [1, 2, 3, 6]
#LAMBDA_VALUES = np.linspace(0.1, 2, 10)  # Valeurs de lambda à tester
LAMBDA_VALUES = np.linspace(0.1, 5, 15)  # Plage de λ pertinente avec 15 points

SIMULATION_TIME = 10000  # Temps total de simulation
CONFIDENCE_LEVEL = 1.96  # Intervalle de confiance à 95%
# Génération de variables exponentielles
def exp_rnd(lmbda):
    return np.random.exponential(1/lmbda)
class Requete:
    def __init__(self, time, category):
        self.time = time  # Temps d'arrivée
        self.category = category  # Catégorie de la requête

class Serveur:
    def __init__(self):
        self.busy = False
        self.end_time = 0

class Routeur:
    def __init__(self, C):
        self.queue = []  # File d'attente FIFO
        self.capacity = QUEUE_SIZE
        self.C = C  # Nombre de groupes
        self.servers = {i: [Serveur() for _ in range(N_SERVEURS // C)] for i in range(C)}
        self.loss_count = 0  # Nombre de requêtes perdues

    def receive_request(self, event_queue, current_time, request):
        if len(self.queue) < self.capacity:
            self.queue.append(request)
            heapq.heappush(event_queue, (current_time + (self.C - 1) / self.C, 'route_request'))
        else:
            self.loss_count += 1  # Requête perdue

    def route_request(self, event_queue, current_time):
        if self.queue:
            request = self.queue.pop(0)
            group = request.category % self.C
            servers = self.servers[group]
            
            for server in servers:
                if not server.busy:
                    server.busy = True
                    service_time = exp_rnd({1: 4/20, 2: 7/20, 3: 10/20, 6: 14/20}[self.C])
                    server.end_time = current_time + service_time
                    heapq.heappush(event_queue, (server.end_time, 'end_service', server, group))
                    return
            
            self.queue.insert(0, request)  # Remet la requête si aucun serveur libre

    def end_service(self, event_queue, current_time, server, group):
        server.busy = False
        if self.queue:
            self.route_request(event_queue, current_time)
def moyenne(data):
    """ calcule la moyenne de la liste data """
    return sum(data) / len(data)

def variance(data):
    """ calcule la variance de la liste data """
    m = moyenne(data)
    data = [(e-m) **2 for e in data]
    return sum(data) / (len(data)-1)

def confidence_interval(data):
    """Calcule la moyenne et la marge d'erreur pour un intervalle de confiance à 95%."""
    if len(data) == 0:
        return 0, 0
    mean = moyenne(data)
    v = variance(data)
    margin = 1.96 * (v / len(data)) ** 0.5  # Marge d'erreur
    return mean, margin

def simulate(C, lmbda):
    event_queue = []
    routeur = Routeur(C)
    current_time = 0
    last_event_time = 0
    request_count = 0
    accepted_requests = 0
    
    total_weighted_requests = 0  # Somme pondérée du nombre de requêtes dans le système
    total_time = 0  # Durée de la simulation (peut être légèrement inférieure à SIMULATION_TIME)

    heapq.heappush(event_queue, (exp_rnd(lmbda), 'arrival'))

    while current_time < SIMULATION_TIME and event_queue:
        current_time, event, *args = heapq.heappop(event_queue)

        # Le nombre de requêtes dans le système
        nb_busy_servers = sum(server.busy for group in routeur.servers.values() for server in group)
        nb_in_queue = len(routeur.queue)
        nb_in_system = nb_busy_servers + nb_in_queue

        # Somme ponderee comme dans le td 2 avec n_cumul
        delta = current_time - last_event_time
        total_weighted_requests += nb_in_system * delta
        last_event_time = current_time

        if event == 'arrival':
            category = np.random.randint(0, C)
            request = Requete(current_time, category)
            prev_loss = routeur.loss_count
            routeur.receive_request(event_queue, current_time, request)
            heapq.heappush(event_queue, (current_time + exp_rnd(lmbda), 'arrival'))
            request_count += 1
            if routeur.loss_count == prev_loss:
                accepted_requests += 1  # Si non perdu

        elif event == 'route_request':
            routeur.route_request(event_queue, current_time)

        elif event == 'end_service':
            server, group = args
            routeur.end_service(event_queue, current_time, server, group)

    total_time = current_time
    L = total_weighted_requests / total_time if total_time else 0
    lambda_effective = accepted_requests / total_time if total_time else 0
    W = L / lambda_effective if lambda_effective else float('inf')
    loss_rate = routeur.loss_count / request_count if request_count else 0
    return W, loss_rate # W est le temps d'attente moyen calcule grace a la loi de Little

# Ajout du code pour tracer le graphique
def plot_response_time():
    results = {C: [] for C in C_VALUES}  # Stocker les résultats pour chaque C

    for C in C_VALUES:
        for lmbda in LAMBDA_VALUES:
            W_values = []
            for _ in range(10):  # Effectuer plusieurs simulations pour réduire la variance
                W, _ = simulate(C, lmbda)
                W_values.append(W)
            mean_W, margin = confidence_interval(W_values)
            results[C].append((lmbda, mean_W, margin))

    # Tracer les courbes
    plt.figure(figsize=(10, 6))
    for C in C_VALUES:
        lambdas = [x[0] for x in results[C]]
        mean_Ws = [x[1] for x in results[C]]
        margins = [x[2] for x in results[C]]
        plt.errorbar(lambdas, mean_Ws, yerr=margins, label=f'C = {C}', capsize=5)

    plt.xlabel('λ (Taux d\'arrivée)')
    plt.ylabel('Temps de réponse moyen (W)')
    plt.title('Temps de réponse moyen (W) en fonction de λ pour différentes valeurs de C')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_loss_rate():
    results = {C: [] for C in C_VALUES}  # Stocker les résultats pour chaque C
    lambda_limits = {}  # Stocker la valeur limite de λ pour chaque C

    for C in C_VALUES:
        for lmbda in LAMBDA_VALUES:
            loss_rates = []
            for _ in range(10):  # Effectuer plusieurs simulations pour réduire la variance
                _, loss_rate = simulate(C, lmbda)
                loss_rates.append(loss_rate)
            mean_loss, margin = confidence_interval(loss_rates)
            results[C].append((lmbda, mean_loss, margin))

            # Déterminer la valeur limite de λ où le taux de perte dépasse 5%
            if mean_loss > 0.05 and C not in lambda_limits:
                lambda_limits[C] = lmbda

    # Tracer les courbes
    plt.figure(figsize=(10, 6))
    for C in C_VALUES:
        lambdas = [x[0] for x in results[C]]
        mean_losses = [x[1] for x in results[C]]
        margins = [x[2] for x in results[C]]
        plt.errorbar(lambdas, mean_losses, yerr=margins, label=f'C = {C}', capsize=5)

    plt.xlabel('λ (Taux d\'arrivée)')
    plt.ylabel('Taux de perte des requêtes')
    plt.title('Taux de perte des requêtes en fonction de λ pour différentes valeurs de C')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Afficher les valeurs limites de λ
    for C, limit in lambda_limits.items():
        print(f"Pour C = {C}, le taux de perte dépasse 5% à partir de λ ≈ {limit:.2f}")

def find_optimal_C_for_lambda_1():
    lambda_target = 1
    optimal_C = None
    best_W = float('inf')  # Initialiser avec une valeur très grande

    print("Résultats pour λ = 1 :")
    for C in C_VALUES:
        W_values = []
        loss_rates = []
        for _ in range(10):  # Effectuer plusieurs simulations pour réduire la variance
            W, loss_rate = simulate(C, lambda_target)
            W_values.append(W)
            loss_rates.append(loss_rate)
        mean_W, _ = confidence_interval(W_values)
        mean_loss, _ = confidence_interval(loss_rates)

        print(f"C = {C} : Temps de réponse moyen (W) = {mean_W:.2f}, Taux de perte = {mean_loss:.2%}")

        # Vérifier si cette valeur de C est meilleure
        if mean_loss <= 0.05 and mean_W < best_W:
            best_W = mean_W
            optimal_C = C

    print(f"\nLe choix optimal de C pour λ = 1 est C = {optimal_C} avec un temps de réponse moyen de {best_W:.2f}.")

def find_optimal_C_for_all_lambdas():
    optimal_choices = {}  # Stocker le choix optimal de C pour chaque λ

    for lmbda in LAMBDA_VALUES:
        optimal_C = None
        best_W = float('inf')  # Initialiser avec une valeur très grande

        print(f"\nRésultats pour λ = {lmbda:.2f} :")
        for C in C_VALUES:
            W_values = []
            loss_rates = []
            for _ in range(10):  # Effectuer plusieurs simulations pour réduire la variance
                W, loss_rate = simulate(C, lmbda)
                W_values.append(W)
                loss_rates.append(loss_rate)
            mean_W, _ = confidence_interval(W_values)
            mean_loss, _ = confidence_interval(loss_rates)

            print(f"C = {C} : Temps de réponse moyen (W) = {mean_W:.2f}, Taux de perte = {mean_loss:.2%}")

            # Vérifier si cette valeur de C est meilleure
            if mean_loss <= 0.05 and mean_W < best_W:
                best_W = mean_W
                optimal_C = C

        if optimal_C is not None:
            optimal_choices[lmbda] = (optimal_C, best_W)
            print(f"Choix optimal pour λ = {lmbda:.2f} : C = {optimal_C} avec W = {best_W:.2f}")
        else:
            print(f"Aucun choix de C ne satisfait les critères pour λ = {lmbda:.2f}")

    return optimal_choices


#Appeler la fonction pour tracer les graphiques
plot_response_time()
plot_loss_rate()

# Appeler la fonction pour déterminer le choix optimal pour λ = 1
find_optimal_C_for_lambda_1()

# Appeler la fonction pour déterminer le choix optimal pour toutes les valeurs de λ
optimal_Cs = find_optimal_C_for_all_lambdas()

# Afficher les résultats finaux
print("\nRésumé des choix optimaux :")
for lmbda, (C, W) in optimal_Cs.items():
    print(f"λ = {lmbda:.2f} : C optimal = {C}, Temps de réponse moyen (W) = {W:.2f}")


