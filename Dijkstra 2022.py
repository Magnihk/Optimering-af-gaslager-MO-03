import heapq
import matplotlib.pyplot as plt
import time
from collections import defaultdict

# Parametre
T = 12  # Totale perioder i måneder
q0 = 5  # Startlager
r = 0.04  # Diskonteringsrate

# Eksempelparametre
q_min = 0  # Min lager per periode
q_max = 10  # Max lager per periode
i_max = 4  # Max ændring per periode
prices = [28.26, 27.23, 42.39, 32.20, 29.17, 33.56, 51.33, 70.04, 59.10, 39.02, 35.72, 36.04]   # Priser per enhed per periode

# Funktion til at beregne profit for en enkelt periode
def period_profit(inventory, change, t):
    new_inventory = inventory + change
    if not (q_min <= new_inventory <= q_max) or abs(change) > i_max:
        return float('-inf'), None  # Ugyldig tilstand
    profit = -change * prices[t]  # Køb er negativ, salg er positiv
    # Diskonter profitten i henhold til din formel
    discount_factor = (1 + r) ** (-t / T)  # Diskonter baseret på tid i forhold til T
    discounted_profit = profit * discount_factor
    return discounted_profit, new_inventory

# Dijkstras algoritme
def optimized_dijkstra():
    best_results = defaultdict(lambda: float('-inf'))
    pq = []  
    heapq.heappush(pq, (0, q0, 0, [q0]))  # Starttilstand
    best_profit = float('-inf')  
    best_path = []  
    while pq:  
        neg_profit, inventory, time_step, path = heapq.heappop(pq)  
        profit = -neg_profit  

        # Hvis vi når den sidste tid, evaluer slutmålet
        if time_step == T:
            # Diskonter slutlageret q_T med e^(-r)
            final_profit = profit + (prices[T-1] * inventory * (1 + r) ** (-1))
            if final_profit > best_profit:
                best_profit = final_profit
                best_path = path
            continue

        # Hvis vi har set en bedre profit for denne tilstand, spring over
        if profit > best_results[(inventory, time_step)]:
            best_results[(inventory, time_step)] = profit
        else:
            continue

        # Udforsk næste tid
        for change in range(-i_max, i_max + 1):
            next_profit, new_inventory = period_profit(inventory, change, time_step)
            if new_inventory is not None:
                heapq.heappush(pq, (-(profit + next_profit), new_inventory, time_step + 1, path + [new_inventory]))

    return best_profit, best_path

# Start timer
start_time = time.time()

# Kør Dijkstras algoritme
max_profit, optimal_path = optimized_dijkstra()

# Slut timer
end_time = time.time()
time_used = end_time - start_time

# Udregner ændringer i lager
changes = [optimal_path[i + 1] - optimal_path[i] for i in range(len(optimal_path) - 1)]

# Udskriver resultater
print("\n=== Resultat ===")
print("Bedste Δq_t sekvens:", changes)
print(f'Den optimale sti er: {optimal_path}')
print("Maksimal diskonteret profit:", max_profit)
print(f"Tid brugt på kørsel: {time_used:.2f} sekunder")

# Plotter resultater
plt.scatter(0, q0, c="black", label="Start Mål")

# Plotter områderne
for t in range(1, T + 1):
    for q in range(q_min, q_max + 1):
        plt.scatter(t, q, c="grey", alpha=0.5)

# Plot optimal sti
plt.plot(range(len(optimal_path)), optimal_path, c="red", label="Optimal Sti")

plt.xlabel("Tid [t]")
plt.ylabel("Lager [q_t]")
plt.title("Optimering af køb og salg af varer")
plt.ylim(q_min, q_max + 1)
plt.legend()
plt.grid(True)
plt.show()
