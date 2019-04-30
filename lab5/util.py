import time
import types
from subprocess import Popen

from decorator import decorator, decorate


def _counterDec(fun, *args, **kwargs):
    c, m = fun.counter, fun.predictedMaxCounter
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


class SubprocessSplitter:
    def __init__(self):
        self.processes = []

    def run(self, name: str):
        p = Popen(['python3', 'graph_subprocess.py', name])
        self.processes.append(p)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for p in self.processes:  # type: Popen
            p.wait()
