import matplotlib.pyplot as plt
import math
import random 
import copy


def scale_to_range(_inp, tmin, tmax):
    inp = copy.deepcopy(_inp)
    min_inp, max_inp = min(inp), max(inp)
    inp_range = max_inp - min_inp
    targ_range = tmax - tmin
    inp = [tmin + ((inp[i] - min_inp) * targ_range) / inp_range for i in range(len(inp))]
    return inp


def pseudorandom(n = 5, duration = 60, range_from = -1, range_to = 1, dt = 0.005):
    L = int(duration / dt)
    disturbance = [0] * L
    for i in range(1, n + 1):
        phase = 2.0 * math.pi * random.random()
        freq = 2.0 * math.pi * i * 0.01 * dt
        disturbance = [disturbance[j] + math.cos(freq * j + phase) for j in range(L)]
    return scale_to_range(disturbance, range_from, range_to)


if __name__ == "__main__":
    for i in range(3):
        plt.plot(pseudorandom(40, 60, -100, 100, dt=0.1))
    plt.show()

