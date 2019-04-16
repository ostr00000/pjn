from collections import defaultdict
from pprint import pprint
from typing import Dict, Union, List, DefaultDict


def levMetric(xStr: str, yStr: str):
    arr = list(range(len(xStr) + 1))
    pprint(arr)

    for i, y in enumerate(yStr, start=1):
        left = i
        skew = i - 1
        oldSim = False
        for j, x in enumerate(xStr, start=1):
            upper = arr[j]

            print(f'comparing: x:({x}, {xStr[j-1:j+1]}) with y:({y}, {yStr[i-1: i+1]})')
            sim = False
            if x == y:
                eq = 0
            elif yStr[i - 1:i + 1] in similarLetters.get(x, ()):
                eq = 0.25
                sim = True
            elif y in similarLetters.get(xStr[j - 1:j + 1], ()):
                eq = 0.25
                sim = True
            elif y in similarLetters.get(x, ()):
                eq = 0.25
            elif oldSim:
                eq = 0
            else:
                eq = 1

            oldSim = sim

            newVal = min((upper + 1, skew + eq, left + 1))
            skew = upper
            left = arr[j] = newVal
        pprint(arr)

    result = arr[-1]
    return result


def updateReversed(data: DefaultDict[str, List[str]]):
    for k, values in list(data.items()):
        for val in values:
            data[val].append(k)
    return data


def stretchMap(data: DefaultDict[str, Union[str, List[str]]]) -> DefaultDict[str, List[str]]:
    for k, v in data.items():
        if not isinstance(v, list):
            data[k] = [v]
    return data


similarLetters = defaultdict(list, **{
    'ą': ['a', 'ę'],
    'ć': 'c',
    'ę': 'e',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ż': 'z',
    'ź': 'z',

    'u': 'ó',

    'rz': 'ż',
    'on': 'ą',
    'om': 'ą',
    'en': 'ę',
    'ch': 'h',
})
similarLetters = updateReversed(stretchMap(similarLetters))

# assert levMetric('biurko', 'pióro') == 2.25
# assert levMetric('abcde', 'ąbćdę') == 0.75
print(levMetric('bende', 'będę'))
# assert levMetric('bende', 'będę') == 0.5

if __name__ == '__main__':
    pass
