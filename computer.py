import math


class Computer:

    # An object which precomputes all distances
    def __init__(self, customers, depots, vehicle):
        together = customers
        together += depots
        self.customers = customers
        self.costliest_edge = -math.inf
        distances = [[] for i in range(len(together))]
        for i in range(len(together)):
            for j in range(len(together)):
                c1 = together[i]
                c2 = together[j]
                distance = Computer.compute_distance(c1, c2)
                if distance > self.costliest_edge:
                    self.costliest_edge = distance
                distances[i].append(distance)
        self.distances = distances
        self.vehicle = vehicle

    def distance_between(self, number1, number2):
        return self.distances[number1 - 1][number2 - 1]

    @staticmethod
    def compute_distance(a, b):
        # Compute distance between two points a and b
        x_diff = a.location.x - b.location.x
        y_diff = a.location.y - b.location.y
        distance = math.sqrt(x_diff * x_diff * y_diff * y_diff)
        return distance

    def compute_route_length(self, list):
        length = 0
        for i in range(len(list)):
            length += self.distance_between(list[i], list[i-1])
        return length

    def fitness_new(self, lists, iteration=1):
        total_distance = 0
        for list in lists:
            length = self.compute_route_length(list)
            total_distance += length + self.punish_illegal_demand(list)
        return total_distance

    def punish_illegal_demand(self, list):
        demand = 0
        cost = 0
        penalty = self.costliest_edge
        customers = [self.customers[i-1] for i in list]
        for customer in customers:
            demand += customer.demand
        if demand > self.vehicle.max_load:
            cost += (demand - self.vehicle.max_load) + penalty
        return cost
