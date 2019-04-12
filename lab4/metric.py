def levMetric(xStr: str, yStr: str):
    arr = list(range(len(xStr) + 1))

    for left, y in enumerate(yStr, start=1):
        skew = left - 1
        for j, x in enumerate(xStr, start=1):
            upper = arr[j]
            eq = 1 if x != y else 0
            newVal = min((upper + 1, skew + eq, left + 1))
            skew = upper
            left = arr[j] = newVal

    result = arr[-1]
    return result


assert levMetric('biurko', 'pióro') == 3
