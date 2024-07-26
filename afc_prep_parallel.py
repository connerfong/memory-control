import numpy as np


def full_waveform_parallel(N, delta, beta, delta_f, num_points, resolution):
    tau = num_points * resolution
    times = np.arange(-tau / 2, tau / 2, resolution)

    theta = np.pi * delta_f / beta * np.log(np.cosh(beta * times))

    # calculate amplitude (and remove not-well-behaved terms
    temp1 = np.sin(N * np.pi * delta * times)
    temp2 = np.sin(np.pi * delta * times)
    for i, val in enumerate(temp2):
        if val == 0:
            temp1[i] = N
            temp2[i] = 1
    amp = temp1 / np.cosh(beta * times) / temp2

    return times, theta, amp


if __name__ == '__main__':
    pass
