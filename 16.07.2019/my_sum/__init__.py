import numpy as np

def sum(arg):
    total = 0
    for val in arg:
        total += val
    return total

print(sum([1,2,3,4,5]))