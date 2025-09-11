
# Giải bài toán 8 quân hậu bằng giải thuật di truyền (không dùng SimpleAI)
import random

N = 8
POP_SIZE = 100
GENERATIONS = 100
MUTATION_RATE = 0.2
TOURNAMENT_SIZE = 3
RUNS = 28

def count_non_attacking_pairs(state):
	count = 0
	for i in range(N):
		for j in range(i + 1, N):
			if abs(state[i] - state[j]) != abs(i - j):
				count += 1
	return count

def fitness(state):
	return count_non_attacking_pairs(state)

def generate_individual():
	state = list(range(N))
	random.shuffle(state)
	return tuple(state)

def tournament_selection(population):
	selected = random.sample(population, TOURNAMENT_SIZE)
	selected.sort(key=lambda x: fitness(x), reverse=True)
	return selected[0]

def crossover(parent1, parent2):
	# PMX crossover
	a, b = sorted(random.sample(range(N), 2))
	child = [None] * N
	child[a:b] = parent1[a:b]
	for i in range(a, b):
		if parent2[i] not in child:
			for j in range(N):
				if child[j] is None and parent2[i] not in child:
					child[j] = parent2[i]
					break
	for i in range(N):
		if child[i] is None:
			for v in parent2:
				if v not in child:
					child[i] = v
					break
	return tuple(child)

def mutate(state):
	state = list(state)
	a, b = random.sample(range(N), 2)
	state[a], state[b] = state[b], state[a]
	return tuple(state)

def genetic_algorithm():
	population = [generate_individual() for _ in range(POP_SIZE)]
	best = max(population, key=fitness)
	for gen in range(GENERATIONS):
		new_population = []
		# Elitism: giữ cá thể tốt nhất
		new_population.append(best)
		while len(new_population) < POP_SIZE:
			parent1 = tournament_selection(population)
			parent2 = tournament_selection(population)
			child = crossover(parent1, parent2)
			if random.random() < MUTATION_RATE:
				child = mutate(child)
			new_population.append(child)
		population = new_population
		current_best = max(population, key=fitness)
		if fitness(current_best) > fitness(best):
			best = current_best
	return best, fitness(best)

if __name__ == "__main__":
	best_state = None
	best_fitness = -1
	for run in range(RUNS):
		state, fit = genetic_algorithm()
		print(f"Run {run+1}: {state}, fitness = {fit}")
		if fit > best_fitness:
			best_fitness = fit
			best_state = state
	print("\nBest solution:", best_state)
	print("Fitness:", best_fitness, "/", N*(N-1)//2)
