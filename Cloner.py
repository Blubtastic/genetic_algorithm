from importer import Dummy


class Cloner:

    # Copy of genome
    @staticmethod
    def clone_genome(genome):
        lists = []
        for list in genome:
            lists.append([Dummy(c.location.x, c.location.y, c.demand) for c in list])

        return lists