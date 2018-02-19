

class ArrayHandler:

    # returns a flattened list + the starting indices of each sublist
    @staticmethod
    def flatten(list_of_indices):
        list = []
        indices = []
        index = 0
        for sublist in list_of_indices:
            list.extend(sublist)
            indices.append(index)
            index += len(sublist)
        indices.append(index)
        return list, indices

    # converts a flattened list to a list of lists
    @staticmethod
    def listify(list, indices):
        list_of_lists = []

        for i in range(1, len(indices)):
            sublist = list[indices[i-1] : indices[i]]
            list_of_lists.append(sublist)
        return list_of_lists
