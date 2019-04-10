import os
from collections import defaultdict
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


def gr(pf: PrimaryForm = None, n=3):
    import regex as re
    LETTERS_PATTERN = re.compile('\P{L}')

    def getWord(word: str):
        try:
            return pf.dictionary[word]
        except KeyError:
            return word

    with open(inputPath) as f:
        d = defaultdict(lambda: 0)

        for j, line in enumerate(f):
            lin = list(filter(None, LETTERS_PATTERN.split(line.rstrip())))
            if not lin:
                continue
            for i in range(0, len(lin) - n):
                if pf:
                    key = tuple(getWord(w.lower()) for w in lin[i:i + n])
                else:
                    key = tuple(w.lower() for w in lin[i:i + n])
                d[key] += 1

            # if j % 1000 == 0:
            #     print(j)

        s = sorted(d.items(), key=itemgetter(1, 0), reverse=True)
        return s


def main():
    primaryForm = PrimaryForm(dictPath)
    ranking = primaryForm.getRankingForFile(inputPath)
    #
    # printFirst(ranking, 50)
    # print(f"Total words: {len(ranking)}")
    # print(f"Hapax legomena: {ranking.countHapaxLegomena()}")
    #
    # printCovering(ranking, 20)
    # printCovering(ranking, 50)
    # printCovering(ranking, 80)
    # printCovering(ranking, 90)
    #
    # plot(ranking)
    #
    # printStatistics(2)
    # printStatistics(3)

    # s = gr(primaryForm, n=3)[:50]
    # print(s)
    # s = gr(primaryForm, n=2)[:50]
    # print(s)
    s = gr(n=3)[:50]
    print(s)
    print("\n")
    s = gr(n=2)[:50]
    print(s)



if __name__ == '__main__':
    main()
