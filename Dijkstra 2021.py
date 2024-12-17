import heapq
import matplotlib.pyplot as plt
import math
from collections import defaultdict

# Parametre
T = 12
q0 = 5
r = 0.04
q_min = [0, 0, 0, 4, 4, 6, 6, 4, 4, 0, 0, 0]
q_max = [10, 10, 10, 10, 8, 8, 8, 8, 10, 10, 10, 10]
u_max = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]
i_max = [4, 4, 2, 2, 1, 1, 1, 1, 2, 2, 4, 4]
P_t = [7.27, 6.16, 6.13, 7.15, 8.91, 10.3, 12.51, 15.43, 22.84, 31.05, 27.62, 38.03]
q_goal = 5
alpha = 0.7

# Opretter en liste over diskonteringsfaktor
discount_factors = [math.exp(-r * (t / T)) for t in range(1, T + 1)]

# Funktion til at beregne profit for en enkelt overgang
def period_profit(inventory, change, t):
    new_inventory = inventory + change
    if not (q_min[t] <= new_inventory <= q_max[t]) or abs(change) > i_max[t]:
        return float('-inf'), None  # Ugyldig overgang
    profit = -change * P_t[t]  # Køb er negativt, salg er positivt
    discount = discount_factors[t - 1] #henter diskonteringsfaktoren
    return profit * discount, new_inventory

# Dijkstra-algoritme
def optimized_dijkstra():
    best_results = defaultdict(lambda: float('-inf'))
    pq = [] #opretter liste til prioritetskø
    heapq.heappush(pq, (0, q0, 0, [q0])) #tilføjer
    best_profit = float('-inf')
    best_path = [] #liste til at lagre bedste vej
    while pq: #mens der er elementer i prioritetskøen
        neg_profit, inventory, time_step, path = heapq.heappop(pq)
        profit = -neg_profit
        if time_step == T: #tjekker om vi er ved sidste periode
            final_profit = profit + P_t[time_step - 1] * inventory * discount_factors[time_step - 1] * (1 if inventory == q_goal else (1 - alpha))
            if final_profit > best_profit:
                best_profit = final_profit
                best_path = path
            continue
        if profit > best_results[(inventory, time_step)]:
            best_results[(inventory, time_step)] = profit
        else:
            continue
        for change in range(-u_max[time_step], i_max[time_step] + 1):
            next_profit, new_inventory = period_profit(inventory, change, time_step)
            if new_inventory is not None:
                heapq.heappush(pq, (-(profit + next_profit), new_inventory, time_step + 1, path + [new_inventory]))
    return best_profit, best_path

# Udfør algoritmen
best_profit, best_path = optimized_dijkstra()

# Beregn ændringer
changes = [best_path[i + 1] - best_path[i] for i in range(len(best_path) - 1)]

# Udskrivelse af resultater
print("\n=== Resultat ===")
print("Bedste Δq_t sekvens:", changes)
print(f'Den optimale sti er: {best_path}')
print("Maksimal diskonteret profit:", best_profit)

# Plot resultater
plt.scatter(0, q0, c="black", label="Start Mål")
for t in range(1, T + 1):
    for q in range(q_min[t - 1], q_max[t - 1] + 1):
        plt.scatter(t, q, c="grey", alpha=0.5)
plt.plot(range(len(best_path)), best_path, c="red", label="Optimal Sti")
plt.xlabel("Tid [t]")
plt.ylabel("Lager [q_t]")
plt.title("Optimering af gaslager")
plt.grid(True)
plt.legend()
plt.show()

