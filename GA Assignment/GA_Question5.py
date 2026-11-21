import random

LOCATIONS = ["A", "B", "C", "D", "E", "F", "G"]
DIST = {
    "A": {"A": 0, "B": 4, "C": 8, "D": 6, "E": 7, "F": 9, "G": 5},
    "B": {"A": 4, "B": 0, "C": 5, "D": 7, "E": 3, "F": 8, "G": 6},
    "C": {"A": 8, "B": 5, "C": 0, "D": 4, "E": 6, "F": 3, "G": 7},
    "D": {"A": 6, "B": 7, "C": 4, "D": 0, "E": 5, "F": 6, "G": 8},
    "E": {"A": 7, "B": 3, "C": 6, "D": 5, "E": 0, "F": 4, "G": 6},
    "F": {"A": 9, "B": 8, "C": 3, "D": 6, "E": 4, "F": 0, "G": 5},
    "G": {"A": 5, "B": 6, "C": 7, "D": 8, "E": 6, "F": 5, "G": 0},
}
DEPOT = "A"
STOPS = ["B", "C", "D", "E", "F", "G"]   # chromosome = permutation of these

SEED = 7               # fixed seed -> reproducible experiment
POP_SIZE = 30
GENERATIONS = 100      # must be >= 50
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.3
ELITE_COUNT = 2        # best routes copied unchanged

random.seed(SEED)

def route_distance(chromosome):
    """Total distance of A -> chromosome -> A (includes return to depot)"""
    full_route = [DEPOT] + chromosome + [DEPOT]
    return sum(DIST[full_route[i]][full_route[i + 1]]
               for i in range(len(full_route) - 1))


def create_individual():
    """A valid chromosome: random permutation of B..G (each exactly once)"""
    route = STOPS[:]
    random.shuffle(route)
    return route


def create_population(size):
    return [create_individual() for _ in range(size)]


def tournament_selection(population):
    """Pick a few random routes and return the shortes/besf of them"""
    contenders = random.sample(population, TOURNAMENT_SIZE)
    return min(contenders, key=route_distance)


def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]          # inherited slice
    fill = [city for city in parent2 if city not in child]  # keep parent2 order
    idx = 0
    for i in range(size):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child


def swap_mutation(chromosome):
    mutant = chromosome[:]
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(mutant)), 2)
        mutant[i], mutant[j] = mutant[j], mutant[i]
    return mutant

def run_ga():
    population = create_population(POP_SIZE)
    best = min(population, key=route_distance)

    for gen in range(1, GENERATIONS + 1):
        population.sort(key=route_distance)

        # Elitism: carry the best routes unchanged into the next generation
        next_gen = [r[:] for r in population[:ELITE_COUNT]]

        # Fill the rest with children of selected parents
        while len(next_gen) < POP_SIZE:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)
            child = order_crossover(p1, p2)
            child = swap_mutation(child)
            next_gen.append(child)

        population = next_gen
        gen_best = min(population, key=route_distance)
        if route_distance(gen_best) < route_distance(best):
            best = gen_best[:]

        if gen == 1 or gen % 10 == 0:
            print(f"Generation {gen:3d}: best distance so far = "
                  f"{route_distance(best)} km")
    return best


if __name__ == "__main__":
    best_route = run_ga()
    print("\n===== RESULT =====")
    print("Best route :", " -> ".join([DEPOT] + best_route + [DEPOT]))
    print("Total distance:", route_distance(best_route), "km")