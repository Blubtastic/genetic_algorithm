import random, math
from importer import Importer
from visualizer import Visualizer
from computer import Computer
from arrayHandler import ArrayHandler
from Cloner import Cloner
import numpy as np


class GeneticAlgorithm:

    def __init__(self, options=None):
        if options is None:
            options = 1
        # Get all customers and depots from selected file
        self.customers, self.depots = Importer.get_data(options)
        self.vehicle = self.depots[0].vehicle
        self.computer = Computer(self.customers, self.depots, self.vehicle)
        self.iteration = 0

    def visualize_genome(self, genome, distance=0):
        customer_locations = [x.location for x in self.customers]
        depot_locations = [x.location for x in self.depots]
        Visualizer.plot(customers=customer_locations, depots=depot_locations, ordered_sets=self.with_depots(genome), distance=distance)

    # Append depots to start and end of route
    def with_depots(self, genome):
        copy_genome = Cloner.clone_genome(genome)
        for i, depot in enumerate(self.depots):
            for vehicle in range(depot.vehicle_count):
                index = i * depot.vehicle_count + vehicle
                copy_genome[index].insert(0, depot)
                copy_genome[index].append(depot)
        return copy_genome

    # Generate "size" random parents.
    def generate_random_population(self, population_size):
        population = []
        for i in range(population_size):
            population.append(self.generate_parent())
        return population

    def fitness_score_new(self, genome):
        lists = []
        for j in range(len(genome)):
            lists.append([x.number for x in genome[j]])
        for i, depot in enumerate(self.depots):
            for vehicle in range(depot.vehicle_count):
                index = i * depot.vehicle_count + vehicle
                lists[index].insert(0, depot.number)
                lists[index].append(depot.number)
        return self.computer.fitness_new(lists, self.iteration)



    def get_lowest_score(self, scores):
        return scores.index(min(scores)), min(scores)

    def fitness_score_depot(self, routes, depot):
        lists = []
        for j in range(len(routes)):
            lists.append([x.number for x in routes[j]])
        for i in range(len(lists)):
            lists[i].insert(0, depot.number)
            lists[i].append(depot.number)
        return self.computer.fitness_new(lists, self.iteration)

    def calculate_indices_for_depot(self, depot_num, genome):
        start = 0
        vehicle_amount = self.depots[depot_num].vehicle_count
        for route in range(0, depot_num * vehicle_amount):
            start += len(genome[route])

        end = start
        for route in range(depot_num * vehicle_amount, depot_num * vehicle_amount + vehicle_amount):
            end += len(genome[route])

        return start, end

    # chooses k random genomes, returns the best
    def select_parent_tournament(self, population, scores, k=5):
        tournament_indices = np.random.choice(len(population), k, replace=False)
        tournament_population = [scores[index] for index in tournament_indices]
        index, score = self.get_lowest_score(tournament_population)
        return population[tournament_indices[index]]

    def crossover(self, parent1, parent2):
        child, child_indices = ArrayHandler.flatten(parent2)
        crossover, crossover_indices = ArrayHandler.flatten(parent1)
        depot_num = random.randint(0, len(self.depots) - 1)

        start, end = self.calculate_indices_for_depot(depot_num, parent2)
        point1 = random.randint(start, end - 1)
        point2 = random.randint(point1, end - 1)
        crossover = crossover[point1:point2]

        for i, element in enumerate(crossover):
            index = child.index(element)
            temp = child[point1 + i]
            child[point1 + i] = child[index]
            child[index] = temp

        child[point1:point2] = crossover
        return ArrayHandler.listify(child, child_indices)

    def crossover_special(self, parent1, parent2):
        child, child_indices = ArrayHandler.flatten(parent2)
        crossover, crossover_indices = ArrayHandler.flatten(parent1)
        point1 = random.randint(0, len(child) - 1)
        point2 = random.randint(point1, len(child) - 1)

        crossover = crossover[point1:point2]

        # swap duplicates before insertion
        for i, element in enumerate(crossover):
            index = child.index(element)
            temp = child[point1 + i]
            child[point1 + i] = child[index]
            child[index] = temp

        child[point1:point2] = crossover
        return ArrayHandler.listify(child, child_indices)



    def mutate_inverse(self, genome):
        # finds a random cut in a random gene (one path) and reverse it
        path_index = random.randint(0, len(genome) - 1)
        if len(genome[path_index]) == 0:
            return self.mutate_inverse(genome)
        start = random.randint(0, len(genome[path_index])-1)
        end = random.randint(0, len(genome[path_index])-1)

        genome[path_index][start:end] = reversed(genome[path_index][start:end])
        return genome

    # swaps two customers from different routes
    def mutate_swap(self, genome):
        # find customer 1
        path_index_1 = random.randint(0, len(genome) - 1)
        if len(genome[path_index_1]) == 0:
            return self.mutate_swap(genome)
        index_1 = random.randint(0, len(genome[path_index_1]) - 1)

        # find customer 2
        path_index_2 = random.randint(0, len(genome[path_index_1]) - 1)
        if len(genome[path_index_2]) == 0:
            return self.mutate_swap(genome)
        index_2 = random.randint(0, len(genome[path_index_2]) - 1)

        # Swap customer 1 with 2
        temp = genome[path_index_1][index_1]
        genome[path_index_1][index_1] = genome[path_index_2][index_2]
        genome[path_index_2][index_2] = temp
        return genome

    def mutate_insertion(self, genome):
        for i in range(random.randint(1, 2)):
            depot_index = random.randint(0, len(self.depots) - 1)
            depot = self.depots[depot_index]

            point = depot_index * depot.vehicle_count
            depot_routes = genome[point: point + depot.vehicle_count]

            route_index = random.randint(0, len(depot_routes) - 1)

            if len(depot_routes[route_index]) == 0:
                return self.mutate_insertion(genome)

            customer_index = random.randint(0, len(depot_routes[route_index]) - 1)
            customer = depot_routes[route_index].pop(customer_index)

            lowest_score = math.inf
            best_route_index = 0
            best_customer_index = 0
            # now, place the customer at all possible locations and calculate where it's best

            for route in range(len(depot_routes)):
                for possible_index in range(len(depot_routes[route]) + 1):

                    depot_routes[route].insert(possible_index, customer)
                    score = self.fitness_score_depot(depot_routes, depot)
                    depot_routes[route].remove(customer)
                    if score < lowest_score:
                        lowest_score = score
                        best_route_index = route
                        best_customer_index = possible_index

            genome[point + best_route_index].insert(best_customer_index, customer)
        return genome

    def mutate_swap_then_insertion(self, genome):
        genome = self.mutate_swap(genome)
        return self.mutate_insertion(genome)

    # Create new genome, when first population is created.
    def generate_parent(self):
        # Genome. Generated "randomly"
        genome = []
        for depot in self.depots:
            for vehicle in range(depot.vehicle_count):
                genome.append([])

        # Calc. all distances to all depots
        distances = []
        for i in range(len(self.depots)):
            distances.append([])
            for j in range(len(self.customers)):
                distances[i].append([j, Computer.compute_distance(self.depots[i], self.customers[j])])
            distances[i].sort(key=lambda tup: tup[1])

        # Add to semi-random route
        depot_count = 0
        for i in range(len(self.customers)):
            index = distances[depot_count][0][0]  # next customer (index in customers)
            rand_vehicle = random.randint(0, self.depots[0].vehicle_count-1)  # next vehicle
            genome_index = depot_count * self.depots[0].vehicle_count + rand_vehicle  # genome
            genome[genome_index].append(self.customers[index])

            # after customer is added, remove it from all lists
            for j in range(len(distances)):
                for k in range(len(distances[j])):
                    if distances[j][k][0] == index:
                        distances[j].pop(k)
                        break
            # go back to 1st depot
            depot_count += 1
            if depot_count >= len(self.depots):
                depot_count = 0

        return genome


# INIT STUFF
ga = GeneticAlgorithm(1)
population_size = 30
iterations = 1
iteration_limit = 1000
crossover_chance = 0.5
# create initial population
population = ga.generate_random_population(population_size)

# MAIN LOOP (ITERATIONS)
while iterations < iteration_limit:
    # calc fitness
    population_scores = [ga.fitness_score_new(g) for g in population]
    score = min(population_scores)

    children = []

    # create new population
    while len(children) < population_size:
        p1 = ga.select_parent_tournament(population, population_scores, k=random.randint(1, 12))
        p2 = ga.select_parent_tournament(population, population_scores, k=random.randint(1, 6))

        for j in range(2):
            if random.random() > crossover_chance:
                if j == 0:
                    child = p1
                elif j == 1:
                    child = p2
            else:
                if random.random() > 0.80:
                    child = ga.crossover_special(p1, p1)
                else:
                    child = ga.crossover(p1, p2)
            fraction = random.random()
            if 0.1 < fraction < 0.35:
                child = ga.mutate_inverse(child)
            if 0.32 < fraction < 0.42:
                child = ga.mutate_swap_then_insertion(child)

            if child not in children:
                children.append(child)
            p1, p2 = p2, p1

    population = children
    if not iterations % 10:
        print("iterations: ", iterations, ". Best score: ", score)

    iterations += 1

ga.visualize_genome(population[0])
