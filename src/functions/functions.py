from math import sqrt,exp,cos,pi


def ackley(axes):
    dim = len(axes)
    sum1 = 0;
    sum2 = 0;

    for x in axes:
        sum1 += x*x
        sum2 += cos(2*pi*x)

    ans = -20 * exp(-0.2 * sqrt((1/dim)*sum1)) - exp((1/dim) * sum2) + 20 + exp(1)
    return ans
