from zhinst.toolkit import Session
from zhinst.toolkit import Waveforms
import numpy as np
import matplotlib.pyplot as plt


def single_tooth(t,d,freq_offset,beta,f_0,w):
    #if np.abs(beta*(t-d)) < np.max:
    temp1 = (np.cos(2*np.pi*(f_0+freq_offset)*d)*np.cos(np.pi*w/beta*np.log(np.cosh(beta*(t-d)))) 
                + np.sin(2*np.pi*(f_0+freq_offset)*d)*np.sin(np.pi*w/beta*np.log(np.cosh(beta*(t-d)))))
    temp2 = (-np.sin(2*np.pi*(f_0+freq_offset)*d)*np.cos(np.pi*w/beta*np.log(np.cosh(beta*(t-d))))
                + np.cos(2*np.pi*(f_0+freq_offset)*d)*np.sin(np.pi*w/beta*np.log(np.cosh(beta*(t-d)))))
    #coefficient for sine term
    c1 = np.cos(2*np.pi*freq_offset*t)*temp1/np.cosh(beta*(t-d))-np.sin(2*np.pi*freq_offset*t)*temp2/np.cosh(beta*(t-d))
    #coefficient for cosine term
    c2 = np.sin(2*np.pi*freq_offset*t)*temp1/np.cosh(beta*(t-d))+np.cos(2*np.pi*freq_offset*t)*temp2/np.cosh(beta*(t-d))
    return (c1,c2)


def full_waveform(N, delta, num_points, resolution, beta, f_0, w):
    tau = num_points*resolution
    teeth = []
    for i in range(N):
        #(freq_offset, center time) of each tooth
        teeth.append((i*delta,i*tau/N))
    times=np.arange(0,num_points*resolution,resolution)
    theta=np.zeros_like(times)
    amp=np.zeros_like(times)

    # c1_total = np.zeros_like(times)
    # c2_total = np.zeros_like(times)
    c1s = []
    c2s = []
    for (freq_offset, d) in teeth:
        offset = d + tau*np.floor((np.abs(times - d) / (tau/2))) * np.sign(times - d)
        (c1, c2) = single_tooth(times,
                                offset,
                                freq_offset, beta, f_0, w)
        # (c1,c2) = (1,0)
        # if t-d > tau/2:
        #     (c1,c2) = single_tooth(t,d+tau,freq_offset,beta,f_0,w)
        # elif t-d < -tau/2:
        #     (c1,c2) = single_tooth(t,d-tau,freq_offset,beta,f_0,w)
        # else:
        #     (c1,c2) = single_tooth(t,d,freq_offset,beta,f_0,w)
        #phase shift at time t
        #print(c1,c2)

        c1s.append(c1)
        c2s.append(c2)

    c1s = np.array(c1s)
    c2s = np.array(c2s)
    c1_tot = np.sum(c1s, axis=0)
    c2_tot = np.sum(c2s, axis=0)

    theta = np.arctan2(c2_tot, c1_tot)

    #amplitude coefficient at time t
    amp = np.sqrt(np.square(c1_tot)+np.square(c2_tot))
        
    return times, theta, amp


if __name__ == '__main__':
    N = 2
    delta = 1e6
    num_points = 10000
    resolution = 1e-9

    test_t, test_theta, test_amp = full_waveform(N, 1e5,100000,1e-8,1e4,300e12,.5e5)

    plt.figure(figsize=(20, 6))
    plt.subplot(131)
    plt.plot(test_t, np.sin(test_theta))
    plt.subplot(132)
    plt.plot(test_t, test_theta)
    plt.subplot(133)
    plt.plot(test_t, test_amp)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
