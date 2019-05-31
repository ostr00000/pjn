import time
import types

from decorator import decorator, decorate


def _counterDec(fun, *args, **kwargs):
    c, m = fun.counter, fun.predictedMaxCounter
    if c == m:
        fun.counter = 0

    if c % 10 == 0:
        print(f"{c}/{m}[{min(100, c/m*100):.3f}%]")

    fun.counter += 1
    return fun(*args, **kwargs)


def counterDecFactory(predictedMaxCounter):
    def counterDec(fun):
        fun.counter = 0
        fun.predictedMaxCounter = predictedMaxCounter
        return decorate(fun, _counterDec)

    return counterDec


@decorator
def timeDec(fun, *args, **kwargs):
    time0 = time.time()
    try:
        return fun(*args, **kwargs)
    finally:
        print(time.time() - time0)


@decorator
def argumentDec(fun, *args, **kwargs):
    values = [f"{fun.__name__}"]
    if args:
        values.append(f"args: {','.join(map(str, args))}")
    if kwargs:
        values.append(f"kwargs: {','.join(f'{k}={v}' for k, v in kwargs.items())}")
    print(', '.join(values))
    return fun(*args, **kwargs)


@decorator
def entryExitDec(fun, *args, **kwargs):
    print(f"Start run function: {fun.__name__}")
    try:
        return fun(*args, **kwargs)
    finally:
        print(f"End run function: {fun.__name__}")


class MetaDec(type):
    def __new__(mcs, name, bases, namespace):
        for valName, valFunc in namespace.items():  # type: str, 'Any'
            if isinstance(valFunc, types.FunctionType) and not valName.startswith('__'):
                namespace[valName] = argumentDec(valFunc)

        return super().__new__(mcs, name, bases, namespace)


class LogIter:
    def __init__(self, val, printStep=100):
        self.val = val
        self.step = printStep

        self.it = None
        self.counter = None

    def __iter__(self):
        self.it = iter(self.val)
        self.counter = 0
        return self

    def __next__(self):
        self.counter += 1
        if self.counter % self.step == 0:
            print(f"iter:{self.counter}")
        return next(self.it)
