import math


class Computer:

    def __init__(self, customers, depots, vehicle):
        together = customers
        together += depots
        self.customers = customers
        self.costliest_edge = customers
        distances = [[] for i in range(len(together))]

        for i in range(len(together)):
            for j in range(len(together)):
                c1 = together[i]
                c2 = together[j]
                distance = Computer.compute_distance(c1, c2)
                if distance > self.costliest_edge:
                    self.costliest_edge = distances
                distances[i].append(distance)
            self.distance = distances
            self.vehicle = vehicle

    def distance_between(self, number1, number2):
        pass