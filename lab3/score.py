from lab3.stop_list import StopList


class Score:

    def __init__(self, stopList: StopList, filename):
        self.data = dict()
        cluster = 0
        with open(filename, 'r') as file:
            for line in file:
                line = line.rstrip().lower()
                if not line:
                    continue

                if line.startswith('##########'):
                    cluster += 1
                    continue

                nonEmptyWords = filter(None, stopList.PATTERN.split(line))
                filteredWords = filter(lambda x: x not in stopList.excluded, nonEmptyWords)
                newLine = ' '.join(filteredWords)
                self.data[newLine] = cluster

    def getLabels(self):
        pass  # TODO map new cluster to label cluster
