import os
from itertools import islice
from operator import itemgetter

from draw import plot
from ngram import NGram
from primary_form import PrimaryForm

dataPath = 'data'
dictPath = os.path.join(dataPath, 'odm.txt')
outputPath = os.path.join(dataPath, 'output.txt')
inputPath = os.path.join(dataPath, 'potop.txt')


def saveConverted(primaryForm):
    with open(outputPath, 'w') as file:
        for text in primaryForm.generate(inputPath, useSeparators=True):
            file.write(text)


def printCovering(ranking, percent):
    print(f"Words which covering {percent}% of text: "
          f"{ranking.getWordsCover(percent)} "
          f"[{100 * ranking.getWordsCover(percent) / len(ranking):.2f}%]")


def printFirst(ranking, firstN=50):
    print(f"First {firstN} most frequent words:\n"
          f"{list(islice(ranking, 0, firstN))}")


def getStatistic(gramNumber):
    nGram = NGram(gramNumber, encoding=None)
    nGram.process(inputPath)
    data = nGram.seqCounter.items()
    data = filter(lambda lettersAndRepeats: len(lettersAndRepeats[0]) == gramNumber, data)
    sortedNGrams = sorted(data, key=itemgetter(1, 0), reverse=True)
    return sortedNGrams


def printStatistics(gramNumber, firstN=20):
    statistic = getStatistic(gramNumber)
    print(f"First {firstN} most frequent {gramNumber}-grams:\n{statistic[:firstN]}")


def main():
    primaryForm = PrimaryForm(dictPath)
    ranking = primaryForm.getRankingForFile(inputPath)

    printFirst(ranking, 50)
    print(f"Total words: {len(ranking)}")
    print(f"Hapax legomena: {ranking.countHapaxLegomena()}")

    printCovering(ranking, 20)
    printCovering(ranking, 50)
    printCovering(ranking, 80)
    printCovering(ranking, 90)

    plot(ranking)

    printStatistics(2)
    printStatistics(3)


if __name__ == '__main__':
    main()
