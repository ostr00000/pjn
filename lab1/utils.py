import time

from decorator import decorator


@decorator
def timeDec(fun, *args, **kwargs):
    start = time.time()
    try:
        return fun(*args, **kwargs)
    finally:
        end = time.time()
        total_time = end - start
        msg = "{name}, execute time:{time:.4f}s" \
            .format(name=fun.__name__, time=total_time)
        print(msg)
