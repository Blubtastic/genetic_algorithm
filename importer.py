import math


class Vehicle:
    def __init__(self, number, max_duration, max_load):
        self.number = number
        self.max_duration = max_duration
        self.max_load = max_load


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Dummy:
    def __init__(self, x, y, demand):
        self.location = Location(x, y)
        self.demand = demand


class Customer:
    def __init__(self, number, x, y, min_service_duration, demand):
        self.number = number
        self.location = Location(x, y)
        self.min_service_duration = min_service_duration
        self.demand = demand


class Depot:
    def __init__(self, number, x, y, vehicle_count, vehicle):
        self.number = number
        self.location = Location(x, y)
        self.vehicle_count = vehicle_count
        self.vehicle = vehicle
        self.demand = 0


# -------- MAIN IMPORTER CLASS --------
# An object w/ the data from one file, containing data about vehicles, customers and depots.
class Importer:

    @staticmethod
    def get_data(file_num):
        number = str(file_num)
        if len(number) == 1: # number < 10
            number = '0' + number

        filename = 'Testing Data/Data Files/p' + number + '.txt'
        file = open(filename, 'r')  # Open selected file, read mode

        line = file.readline()  # Read 1st line
        line = line.replace('\n', '').split(' ')  # splir the line into 3
        vehicle_count = int(line[0])  # vehicles per depot
        customer_count = int(line[1])
        depot_count = int(line[2])
        print('Customers', customer_count, '  Depots', depot_count, '  Vehicles', vehicle_count)

        # Generate the representation. (Objects for vehicles, customers & depots)
        vehicles = []
        customers = []
        depots = []
        # vehicles
        for i in range(1, depot_count + 1):
            line = file.readline().replace('\n', '').strip().split(' ')  # make a list of all numbers
            max_duration = int(line[0])
            if max_duration == 0:
                max_duration = math.inf
            max_load = int(line[1])
            vehicle = Vehicle(i, max_duration, max_load)  # new vehicle
            vehicles.append(vehicle)
        # customers
        for i in range(1, customer_count + 1):
            line = file.readline().replace('\n', '').split(' ')
            line = [s for s in line if len(s) != 0]  # remove empty spaces in list
            number = int(line[0])
            x = int(line[1])
            y = int(line[2])
            min_service_duration = int(line[3])
            demand = int(line[4])
            customer = Customer(number, x, y, min_service_duration, demand)  # new customer
            customers.append(customer)
        # depots
        for i in range(1, depot_count + 1):
            line = file.readline().replace('\n', '').split(' ')
            line = [s for s in line if len(s) != 0]  # remove empty spaces in list
            number = int(line[0])
            x = int(line[1])
            y = int(line[2])
            # new depot with vehicle_count number of vehicles.
            depot = Depot(number, x, y, vehicle_count, vehicles[i-1])
            depots.append(depot)
        return customers, depots
