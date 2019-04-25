from collections import defaultdict

from typing import Union, DefaultDict, Set


def levMetric(xStr: str, yStr: str):
    arr = list(range(len(xStr) + 1))
    result = None
    doubleWordLoop = False
    for i, y in enumerate(yStr, start=1):
        left = i
        skew = i - 1
        doubleWord = False

        if doubleWordLoop:
            doubleWordLoop = False
            continue
        doubleWordLoop = False

        for j, x in enumerate(xStr, start=1):
            upper = arr[j]
            leftInc = 0 if doubleWord else 1
            doubleWord = False

            # advanced option
            if x == y:
                eq = 0
            elif len(yStr[i - 1:i + 1]) == 2 and yStr[i - 1:i + 1] in similarLetters.get(x, ()):
                eq = 0.25
                doubleWordLoop = True
            elif len(xStr[j - 1:j + 1]) == 2 and y in similarLetters.get(xStr[j - 1:j + 1], ()):
                eq = 0.25
                doubleWord = True
            elif y in similarLetters.get(x, ()):
                eq = 0.25
            else:
                eq = 1

            # simple option
            # eq = 1 if x != y else 0

            newVal = min((upper + 1, skew + eq, left + leftInc))
            skew = upper
            left = arr[j] = newVal

        if doubleWord:
            result = arr[-1]

    result = min(arr[-1], result) if result else arr[-1]
    return result


def updateReversed(data: DefaultDict[str, Set[str]]):
    for k, values in list(data.items()):
        for val in values:
            data[val].add(k)
    return dict(data)


def convertValuesToSet(data: DefaultDict[str, Union[str, Set[str]]]) -> DefaultDict[str, Set[str]]:
    for k, v in data.items():
        if not isinstance(v, set):
            data[k] = {v}
    return data


similarLetters = defaultdict(set, **{
    'ą': {'a', 'ę'},
    'ć': 'c',
    'ę': 'e',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ż': 'z',
    'ź': 'z',
    'ł': 'l',

    'u': 'ó',

    'rz': 'ż',
    'on': 'ą',
    'om': 'ą',
    'en': 'ę',
    'ch': 'h',
})
similarLetters = updateReversed(convertValuesToSet(similarLetters))

if __name__ == '__main__':
    # equality
    assert levMetric('simpleword', 'simpleword') == 0
    assert levMetric('si', 'si') == 0
    assert levMetric('a', 'a') == 0

    # size diff
    assert levMetric('simpleword', 'simpleword++') == 2
    assert levMetric('simpleword--', 'simpleword') == 2
    assert levMetric('simpleword', 'simpl++eword') == 2
    assert levMetric('simpl--eword', 'simpleword') == 2
    assert levMetric('simpleword', '++simpleword') == 2
    assert levMetric('--simpleword', 'simpleword') == 2

    # spelling error
    assert levMetric('tą', 'tę') == 0.25
    assert levMetric('ów', 'uw') == 0.25
    assert levMetric('ktoś', 'któs') == 0.5

    # size error without prefix and suffix
    assert levMetric('en', 'ę') == 0.25
    assert levMetric('ę', 'en') == 0.25
    assert levMetric('ku', 'q') == 2
    assert levMetric('q', 'ku') == 2

    # size error good prefix
    assert levMetric('ben', 'bę') == 0.25
    assert levMetric('bę', 'ben') == 0.25
    assert levMetric('bq', 'bku') == 2
    assert levMetric('bku', 'bq') == 2

    # size error bad prefix
    assert levMetric('den', 'bę') == 1.25
    assert levMetric('dę', 'ben') == 1.25
    assert levMetric('dku', 'bq') == 3
    assert levMetric('dq', 'bku') == 3

    # size error good suffix
    assert levMetric('end', 'ęd') == 0.25
    assert levMetric('ęd', 'end') == 0.25
    assert levMetric('kud', 'qd') == 2
    assert levMetric('qd', 'kud') == 2

    # size error bad suffix
    assert levMetric('end', 'ęc') == 1.25
    assert levMetric('ęd', 'enc') == 1.25
    assert levMetric('kud', 'qc') == 3
    assert levMetric('qd', 'kuc') == 3

    # size error two times
    assert levMetric('aendenc', 'aędęc') == 0.5
    assert levMetric('aędęc', 'aendenc') == 0.5
    assert levMetric('akudkuc', 'aqdqc') == 4
    assert levMetric('aqdqc', 'akudkuc') == 4

    # size error two times in row
    assert levMetric('żż', 'rzrz') == 0.5
    assert levMetric('rzrz', 'żż') == 0.5

    # other
    assert levMetric('biurko', 'pióro') == 2.25
    assert levMetric('abcde', 'ąbćdę') == 0.75
    assert levMetric('bende', 'będę') == 0.5
    assert levMetric('gżegżółka', 'grzegrzulka') == 1
    assert levMetric('bendórzę', 'będużą') == 1    # en -> ę, ó -> u, rz -> ż, ę -> ą

