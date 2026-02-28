import warnings

def deprecated(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@deprecated('Ne nado menya ispolzovat plez')
def f(x):
    return x

@deprecated('I am good')
def g(x):
    return x-2

print(f(1), g(5))