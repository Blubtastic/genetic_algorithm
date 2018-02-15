import random, math
from importer import Importer
from visualizer import Visualizer
from computer import Computer
from arrayHandler import ArrayHandler
from Cloner import Cloner
import numpy as np


class GeneticAlgorithm():

    def __init__(self, options=None):
        if options is None:
            options = 1
        # Get all customers and depots from selected file
        self.customers, self.depots = Importer.get_data(options)
        print([x.demand for x in self.customers])


GeneticAlgorithm()