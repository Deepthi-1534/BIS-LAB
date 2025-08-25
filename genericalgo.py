import random

# Step 1: Initialize Population
def initialize_population(num_individuals, cities):
    return [random.sample(cities, len(cities)) for _ in range(num_individuals)]

# Step 2: Calculate total distance of a tour
def calculate_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour)):
        total_distance += distance_matrix[tour[i - 1]][tour[i]]  # cyclic path
    return total_distance

# Step 2: Calculate fitness (1 / distance)
def calculate_fitness(population, distance_matrix):
    fitness_scores = []
    for individual in population:
        dist = calculate_distance(individual, distance_matrix)
        fitness_scores.append(1 / dist)
    return fitness_scores

# Step 3: Roulette Wheel Selection
def roulette_wheel_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fitness in zip(population, fitness_scores):
        current += fitness
        if current > pick:
            return individual

# Step 4: Order Crossover (OX)
def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    
    offspring = [None] * size
    offspring[start:end+1] = parent1[start:end+1]
    
    pointer = 0
    for city in parent2:
        if city not in offspring:
            while offspring[pointer] is not None:
                pointer += 1
            offspring[pointer] = city
    
    return offspring

# Step 5: Swap Mutation
def swap_mutation(tour, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

# Step 6: Create New Generation
def create_new_generation(population, fitness_scores, mutation_rate):
    new_population = []
    population_size = len(population)
    
    while len(new_population) < population_size:
        parent1 = roulette_wheel_selection(population, fitness_scores)
        parent2 = roulette_wheel_selection(population, fitness_scores)
        
        offspring1 = order_crossover(parent1, parent2)
        offspring2 = order_crossover(parent2, parent1)
        
        offspring1 = swap_mutation(offspring1, mutation_rate)
        offspring2 = swap_mutation(offspring2, mutation_rate)
        
        new_population.append(offspring1)
        if len(new_population) < population_size:
            new_population.append(offspring2)
    
    return new_population

# Main Genetic Algorithm
def genetic_algorithm_tsp(cities, distance_matrix, population_size=100, mutation_rate=0.02, max_generations=500):
    population = initialize_population(population_size, cities)
    best_solution = None
    best_distance = float('inf')
    
    for generation in range(max_generations):
        fitness_scores = calculate_fitness(population, distance_matrix)
        
        # Track the best solution
        for i, individual in enumerate(population):
            dist = 1 / fitness_scores[i]
            if dist < best_distance:
                best_distance = dist
                best_solution = individual
        
        print(f"Generation {generation+1}: Best Distance = {best_distance:.4f}")
        
        population = create_new_generation(population, fitness_scores, mutation_rate)
    
    return best_solution, best_distance

# Example Usage
if __name__ == "__main__":
    # Example cities indexed 0 to 4
    cities = [0, 1, 2, 3, 4]
    
    # Example symmetric distance matrix (5 cities)
    distance_matrix = [
        [0, 2, 9, 10, 7],
        [2, 0, 6, 4, 3],
        [9, 6, 0, 8, 5],
        [10, 4, 8, 0, 6],
        [7, 3, 5, 6, 0]
    ]
    
    best_tour, best_dist = genetic_algorithm_tsp(cities, distance_matrix, population_size=50, mutation_rate=0.05, max_generations=100)
    print("Best Tour:", best_tour)
    print("Best Distance:", best_dist)
