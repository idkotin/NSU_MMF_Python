import warnings

def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn("Dont use me! :(")
        return func(*args, **kwargs)
    return wrapper

@deprecated
def f(x):
    return x

print(f(1))