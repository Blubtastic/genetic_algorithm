import matplotlib.pyplot as plt
import random
from computer import Computer


class Visualizer:
    plt.figure(num=None, figsize=(14, 9), dpi=100, facecolor='w', edgecolor='k')

    # init-ish
    @staticmethod
    def plot(customers, depots, ordered_sets=None, distance=0):
        Visualizer.show_items(customers, color='blue', marker='o')
        Visualizer.show_items(depots, color='red', marker='x')
        # when we have a possible solution, this must be shown as requested in the assignment
        if ordered_sets:
            i = 0
            for set in ordered_sets:
                locations = [x.location for x in set]
                if i >= len(ordered_sets):
                    break
                r = lambda: random.randint(0, 255)
                r = '#%02X%02X%02X' % (r(), r(), r())
                Visualizer.show_items(locations, color=r, scatter=False)
                i += 1
            pass
        plt.title('Distance: %i meters' %distance)
        plt.ioff()
        plt.show()

    # Draw element
    @staticmethod
    def show_items(items, marker='x', color='blue', scatter=True):
        x = []
        y = []
        for item in items:
            x.append(item.x)
            y.append(item.y)
        if scatter:
            plt.scatter(x, y, edgecolors=color, marker=marker)
        else:
            plt.plot(x, y, color=color, linewidth=0.7)

    # Wtf is dis?
    @staticmethod
    def textual_representation(genetic_algorithm, genome, score):
        print(score)
        for i, depot in enumerate(genetic_algorithm.depots):
            for vehicle in range(depot.vehicle_count):
                path = genome[i * depot.vehicle_count * vehicle]
                route_duration = Computer.compute_path_length(path)
                route_demand = Computer.compute_route_demand(i * depot.vehicle_count + vehicle,genome)
                route = [str(i.number) for i in path]
                route.insert(0, "0")
                route.append("0")
                print('%d\t%d\t%.2f\t%d\t' % (i+1, vehicle+1, route_duration, route_demand), end='')
                print(' '.join(route))

        pass
