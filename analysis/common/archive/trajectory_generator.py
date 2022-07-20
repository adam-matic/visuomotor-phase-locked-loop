import math
import random
import numpy as np
import scipy.interpolate as interpolate


def rose(k=1/2, pi_N=2, x=0, y=0, size=100, steps_N = 500):
    step = pi_N * math.pi / steps_N
    phis = [step * i for i in range(steps_N)]
    return [((x + size * math.cos(k * phi) * math.cos(phi)), (y + size * math.cos(k * phi) * math.sin(phi))) for phi in phis]

def circle(x, y, r, steps_N):
    step = 2 * math.pi / steps_N
    phis = [step * i for i in range(steps_N)]
    return [(x + r * math.cos(angle), (y + r * math.sin(angle))) for angle in phis]

def ellipse(x, y, axis_ratio, size, steps_N=500):
    step = 2 * math.pi / steps_N
    phis = [step * i for i in range(steps_N)]
    A = size; B = A * axis_ratio
    return [(x + A * math.cos(angle), (y + B * math.sin(angle))) for angle in phis]

def pseudorandom(maxdata, difficulty, total_range):
    d = [2.2 / 16, 2.2 / 22.6, 2.2 / 32, 2.2 / 45.25, 2.2 / 64, 2.2/128]
    dslow = d[difficulty]
    dtable = [0] * maxdata
    # generate and add 120 waves with increasing freq and random phase shifts
    for n in range(1, 120):
        phase = 2.0 * math.pi * random.random()
        amplitude = math.exp(-0.7 * dslow * n)
        temp = 2.0 * math.pi * n / 4000
        for i in range(maxdata): dtable[i] = dtable[i] + amplitude * math.cos(temp * i + phase)
    mx = max(dtable)
    mn = min(dtable)

    # center around 0 and scale to required range
    rng = mx - mn
    half = (mx + mn) / 2.0
    for i in range(maxdata): dtable[i] = (dtable[i] - half) / rng * 0.95 * total_range
    return np.asarray(dtable)

def pure_curve_trajectory(x0=0, y0=0, eps=1.2, v=2, th0=0, N=2, scale=220, beta=2.0 / 3.0, k=2, time_dt=0.005):
    xs, ys, theta = [], [], []
    dtheta = 0.001
    x,y = x0, y0
    th = 0
    while (th < math.pi * N):
        dx = dtheta * math.cos(th) * math.exp(eps * math.sin(v * (th - th0)))
        x = x + scale * dx
        dy = dtheta * math.sin(th) * math.exp(eps * math.sin(v * (th - th0)))
        y = y + scale * dy
        th = th + dtheta
        xs.append(x)
        ys.append(y)
        theta.append(th)

    R_exp_beta = np.exp(beta * eps * np.sin(v * np.subtract(theta, th0)))

    t = 0
    t_theta = []
    for i in range(0, len(theta)):
        t = t + dtheta * R_exp_beta[i] / k
        t_theta.append(t)

    new_time = np.arange(0, t, time_dt)

    xspl = interpolate.UnivariateSpline(t_theta, xs, k=3, s=0)
    yspl = interpolate.UnivariateSpline(t_theta, ys, k=3, s=0)
    xo = xspl(new_time)
    yo = yspl(new_time)
    
    res = trajectory(xo, yo, new_time)
    
    return res


def time_profile(elements, element_order, segment_len, transition_len, dt=0.001):
    time_profile = []
    N = len(element_order) 
    sN = int(segment_len/dt)
    tN = int(transition_len/dt)
    total_time = N * segment_len + (N - 1) * transition_len
    def e(n): return elements[element_order[n]]
    for i in range(N-1): time_profile += [e(i)] * sN + list(np.linspace(e(i), e(i+1), tN))
    time_profile += [e(N-1)] * sN

    ts = np.arange(len(time_profile)) * dt
    element_time_function = interpolate.UnivariateSpline(ts, time_profile, k=3, s=0)
    return element_time_function



if __name__ == '__main__':
    import time
    import matplotlib.pyplot as plt

    t1 = time.perf_counter()
    
    v1 = newWave(6000, 0, 800)
    v2 = pseudorandom(6000, 0, 800)

    print(time.perf_counter() - t1)

    plt.plot(v1)

    plt.plot(v2)
    plt.show()



