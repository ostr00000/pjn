import matplotlib.pyplot as plt
import numpy as np

from ranking import Ranking


def plot(ranking: Ranking):
    y = np.array([r[1] for r in ranking])
    x = np.arange(1, y.size + 1)

    const = y[0]
    r = const / x

    plt.plot(x, y, label="f(word_ranking)=word_frequency")
    plt.plot(x, r, label="f(x)=c/x")

    plt.yscale('log')
    plt.title("Zipf law")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.legend(loc='upper right')
    plt.show()
