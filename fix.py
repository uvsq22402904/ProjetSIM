import heapq
import numpy as np
import matplotlib.pyplot as plt


# Paramètres globaux
N_SERVEURS = 12
QUEUE_SIZE = 100
C_VALUES = [1, 2, 3, 6]
LAMBDA_VALUES = np.arange(0.1, 6, 0.35)
SIMULATION_TIME = 1000


def exp_rnd(lmbda):
    return np.random.exponential(1 / lmbda)

class Requete:
    def __init__(self, time, category):
        self.time = time
        self.category = category

class Serveur:
    def __init__(self):
        self.busy = False
        self.end_time = 0

class Routeur:
    def __init__(self, C):
        self.C = C
        self.queue = []
        self.capacity = QUEUE_SIZE
        self.busy = False
        self.servers = {i: [Serveur() for _ in range(N_SERVEURS // C)] for i in range(C)}
        self.loss_count = 0
        self.completed = 0  # Compteur de requêtes complétées
        self.queue_blocked = False  # Indique si la file est bloquée en attente d'un serveur
        self.waiting_category = None  # Catégorie pour laquelle on attend un serveur libre

    def receive_request(self, event_queue, now, request):
        if len(self.queue) < self.capacity:
            self.queue.append(request)
            if not self.busy and not self.queue_blocked:
                self.start_routing(event_queue, now)
        else:
            self.loss_count += 1

    def start_routing(self, event_queue, now):
        if self.queue and not self.queue_blocked:
            self.busy = True
            delay = (self.C - 1) / self.C
            heapq.heappush(event_queue, (now + delay, 'end_routing'))

    def end_routing(self, event_queue, now):
        self.busy = False
        request = self.queue.pop(0)
        
        # Essayer de dispatcher la requête vers un serveur libre
        if self.dispatch_to_server(event_queue, now, request):
            # Si dispatch réussi et file pas bloquée, continuer avec la prochaine requête
            if self.queue and not self.queue_blocked:
                self.start_routing(event_queue, now)
        else:
            # Si pas de serveur disponible, bloquer la file et mettre la requête en attente
            self.queue_blocked = True
            self.waiting_category = request.category
            # Remettre la requête en tête de file
            self.queue.insert(0, request)

    def dispatch_to_server(self, event_queue, now, request):
        group = request.category
        servers = self.servers[group]
        
        # Chercher un serveur libre dans le groupe correspondant
        for srv in servers:
            if not srv.busy:
                srv.busy = True
                rate = {1: 4/20, 2: 7/20, 3: 10/20, 6: 14/20}[self.C]
                service_time = exp_rnd(rate)
                srv.end_time = now + service_time
                heapq.heappush(event_queue, (srv.end_time, 'end_service', srv, group, request))
                return True  # Dispatch réussi
                
        return False  # Pas de serveur disponible

    def end_service(self, event_queue, now, server, group, request):
        self.completed += 1
        server.busy = False
        
        # Si la file était bloquée en attente de ce groupe de serveurs
        if self.queue_blocked and self.waiting_category == group:
            # Essayer de traiter la requête en attente
            if self.queue:
                req = self.queue[0]
                if req.category == group and self.dispatch_to_server(event_queue, now, req):
                    # Requête traitée, la retirer de la file
                    self.queue.pop(0)
                    
                    # Si la file n'est plus vide, vérifier si on peut continuer à router
                    if self.queue:
                        # Vérifier si la prochaine requête est pour un groupe disponible
                        next_req = self.queue[0]
                        can_process = False
                        for srv in self.servers[next_req.category]:
                            if not srv.busy:
                                can_process = True
                                break
                        
                        if can_process:
                            # Débloquer la file et commencer à router
                            self.queue_blocked = False
                            self.waiting_category = None
                            if not self.busy:
                                self.start_routing(event_queue, now)
                    else:
                        # File vide, débloquer
                        self.queue_blocked = False
                        self.waiting_category = None

def simulate(C, lmbda):
    event_queue = []
    routeur = Routeur(C)
    now = 0
    last = 0
    request_count = 0
    total_weighted = 0

    heapq.heappush(event_queue, (exp_rnd(lmbda), 'arrival'))

    while now < SIMULATION_TIME and event_queue:
        event_tuple = heapq.heappop(event_queue)
        now = event_tuple[0]
        event = event_tuple[1]
        args = event_tuple[2:]

        # Calcul des statistiques
        busy = sum(srv.busy for grp in routeur.servers.values() for srv in grp)
        total_weighted += (busy + len(routeur.queue)) * (now - last)
        last = now

        if event == 'arrival':
            category = np.random.randint(0, C)
            req = Requete(now, category)
            routeur.receive_request(event_queue, now, req)
            heapq.heappush(event_queue, (now + exp_rnd(lmbda), 'arrival'))
            request_count += 1

        elif event == 'end_routing':
            routeur.end_routing(event_queue, now)

        elif event == 'end_service':
            srv, grp, req = args
            routeur.end_service(event_queue, now, srv, grp, req)

    total_time = now
    L = total_weighted / total_time if total_time else 0
    lambda_eff = routeur.completed / total_time if total_time else 0
    W = L / lambda_eff if lambda_eff else float('inf')
    loss_rate = routeur.loss_count / request_count if request_count else 0
    return W, loss_rate

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

def run_all_simulations():
    results = {C: [] for C in C_VALUES}
    lambda_limits = {}
    for C in C_VALUES:
        for lmbda in LAMBDA_VALUES:
            W_values = []
            loss_rates = []
            for _ in range(10):
                W, loss_rate = simulate(C, lmbda)
                W_values.append(W)
                loss_rates.append(loss_rate)
            mean_W, W_margin = confidence_interval(W_values)
            mean_loss, loss_margin = confidence_interval(loss_rates)
            results[C].append((lmbda, mean_W, W_margin, mean_loss, loss_margin))
            if mean_loss > 0.05 and C not in lambda_limits:
                lambda_limits[C] = lmbda
    return results, lambda_limits

def plot_response_time(results):
    plt.figure(figsize=(10, 6))
    for C in C_VALUES:
        lambdas = [x[0] for x in results[C]]
        mean_Ws = [x[1] for x in results[C]]  # Mean response time
        margins = [x[2] for x in results[C]]  # Margin for response time
        plt.errorbar(lambdas, mean_Ws, yerr=margins, label=f'C = {C}', capsize=5)
    plt.xlabel('λ (Taux d\'arrivée)')
    plt.ylabel('Temps de réponse moyen (W)')
    plt.title('Temps de réponse moyen (W) en fonction de λ pour différentes valeurs de C')
    plt.legend()
    plt.grid(True)
    plt.savefig('response_time_plot.png', dpi=300, bbox_inches='tight')  # Save as PNG
    plt.show()
    plt.close()  # Close the figure to free memory

def plot_loss_rate(results, lambda_limits):
    plt.figure(figsize=(10, 6))
    for C in C_VALUES:
        lambdas = [x[0] for x in results[C]]
        mean_losses = [x[3] for x in results[C]]  # Mean loss rate
        margins = [x[4] for x in results[C]]      # Margin for loss rate
        plt.errorbar(lambdas, mean_losses, yerr=margins, label=f'C = {C}', capsize=5)
    plt.xlabel('λ (Taux d\'arrivée)')
    plt.ylabel('Taux de perte des requêtes')
    plt.title('Taux de perte des requêtes en fonction de λ pour différentes valeurs de C')
    plt.legend()
    plt.grid(True)
    plt.savefig('loss_rate_plot.png', dpi=300, bbox_inches='tight')  # Save as PNG
    plt.show()
    plt.close()  # Close the figure to free memory

    # Afficher les valeurs limites de λ
    for C, limit in lambda_limits.items():
        print(f"Pour C = {C}, le taux de perte dépasse 5% à partir de λ ≈ {limit:.2f}")

def find_optimal_C_for_lambda_1(results):
    lambda_target = 1
    optimal_C = None
    best_W = float('inf')  # Initialiser avec une valeur très grande

    print("Résultats pour λ = 1 :")
    for C in C_VALUES:
        # Trouver l'entrée correspondant à lambda_target dans results[C]
        for entry in results[C]:
            if abs(entry[0] - lambda_target) < 1e-6:  # Comparaison flottante
                mean_W = entry[1]    # Temps de réponse moyen
                mean_loss = entry[3] # Taux de perte moyen
                print(f"C = {C} : Temps de réponse moyen (W) = {mean_W:.2f}, Taux de perte = {mean_loss:.2%}")

                # Vérifier si cette valeur de C est meilleure
                if mean_loss <= 0.05 and mean_W < best_W:
                    best_W = mean_W
                    optimal_C = C
                break  # Sortir après avoir trouvé l'entrée correspondante

    if optimal_C is not None:
        print(f"\nLe choix optimal de C pour λ = 1 est C = {optimal_C} avec un temps de réponse moyen de {best_W:.2f}.")
    else:
        print("\nAucun choix de C ne satisfait les critères pour λ = 1.")

def find_optimal_C_for_all_lambdas(results, lambda_limits):
    optimal_choices = {}  # Stocker le choix optimal de C pour chaque λ

    for lmbda in LAMBDA_VALUES:
        optimal_C = None
        best_W = float('inf')  # Initialiser avec une valeur très grande

        print(f"\nRésultats pour λ = {lmbda:.2f} :")
        for C in C_VALUES:
            # Trouver l'entrée correspondant à lmbda dans results[C]
            for entry in results[C]:
                if abs(entry[0] - lmbda) < 1e-6:  # Comparaison flottante
                    mean_W = entry[1]    # Temps de réponse moyen
                    mean_loss = entry[3] # Taux de perte moyen
                    print(f"C = {C} : Temps de réponse moyen (W) = {mean_W:.2f}, Taux de perte = {mean_loss:.2%}")

                    # Vérifier si cette valeur de C est meilleure
                    if mean_loss <= 0.05 and mean_W < best_W:
                        best_W = mean_W
                        optimal_C = C
                    break  # Sortir après avoir trouvé l'entrée correspondante

        if optimal_C is not None:
            optimal_choices[lmbda] = (optimal_C, best_W)
            print(f"Choix optimal pour λ = {lmbda:.2f} : C = {optimal_C} avec W = {best_W:.2f}")
        else:
            print(f"Aucun choix de C ne satisfait les critères pour λ = {lmbda:.2f}")

    # Afficher les valeurs limites de λ pour chaque C
    print("\nValeurs limites de λ où le taux de perte dépasse 5% :")
    for C, limit in lambda_limits.items():
        print(f"Pour C = {C}, le taux de perte dépasse 5% à partir de λ ≈ {limit:.2f}")

    return optimal_choices


if __name__ == "__main__":
    results, lambda_limits = run_all_simulations()
    plot_response_time(results)
    plot_loss_rate(results, lambda_limits)
    find_optimal_C_for_lambda_1(results)
    optimal_Cs = find_optimal_C_for_all_lambdas(results, lambda_limits)

    # Afficher les résultats finaux
    print("\nRésumé des choix optimaux :")
    for lmbda, (C, W) in sorted(optimal_Cs.items()):
        print(f"λ = {lmbda:.2f} : C optimal = {C}, Temps de réponse moyen (W) = {W:.2f}")