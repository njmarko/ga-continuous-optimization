from math import sqrt, exp, sin, cos, pi, pow


def ackley(axis):
    dim = len(axis)
    sum1 = 0
    sum2 = 0

    for x in axis:
        sum1 += x * x
        sum2 += cos(2 * pi * x)

    ans = -20 * exp(-0.2 * sqrt((1 / dim) * sum1)) - exp((1 / dim) * sum2) + 20 + exp(1)
    return ans


def griewank(axis):
    sum1 = 0
    product1 = 1

    for i, x in enumerate(axis):
        sum1 += (x * x) / 4000
        product1 *= cos(x / sqrt(i + 1))

    ans = sum1 - product1 + 1
    return ans


def michalewicz(axis):
    sum1 = 0

    for i, x in enumerate(axis):
        sum1 += sin(x) * pow(sin(((i + 1) * x * x) / pi), 20)

    ans = -sum1
    return ans
