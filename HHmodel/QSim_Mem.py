from QHH_3 import QHH_3
import numpy as np
import matplotlib.pyplot as plt
from q_memristor.numerical import num_memristor

"""
    Comparison of Quantized three-ion-channel Hodgkin-Huxley model with new Quantum Memristor
    
    Author: Chiara Paglioni
"""

if __name__ == "__main__":
    qhh = QHH_3()

    eps = 0.0001
    tmax = 10
    ts = np.arange(0, tmax, eps)
    Zk = np.zeros(len(ts))
    ZNa = np.zeros(len(ts))

    # Spike try parameters
    Cc = 10 ** (-6)
    Cg = 10 ** (-6)
    Cr = 10 ** (-6)

    # Impedance of the outgoing transmission line
    Zout = 50

    # Activation variable values
    n0 = 0.4
    m0 = 0.6
    h0 = 0.2

    # Initial update of the system
    # Chloride channel = constant = 1 / GCl
    # GCl = 3 * 10^-4
    ZL = 1 / (3 * 10 ** (-4))
    # Chloride channel = constant = 1 / GK
    # GK = max potassium conductance * m0^4
    Zk[0] = 1 / (1.33 * (n0 ** 4))
    # Chloride channel = constant = 1 / GNa
    # GNa = max sodium conductance * m0^3 * h0
    ZNa[0] = 1 / (0.17 * (m0 ** 3) * h0)

    w = np.full((len(ts)), 10)
    I0 = np.full((len(ts)), 1)
    I0[:int(len(ts) / 4)] = 0
    w[:int(len(ts) / 4)] = 0

    # Input current of the system
    I = np.multiply(I0, np.sin(np.multiply(w, ts)))

    # Memristor simulation parameters
    a = np.pi/4
    b = np.pi/5
    m = 1
    h = 1
    w_m = 1
    y0 = 0.4

    mem = num_memristor.memristor(y0, w_m, h, m, a, b)

    # Voltage
    Vm = np.zeros(len(ts))
    Vm[0] = qhh.V(Zk[0], ZNa[0], ZL, Zout, I0[0], w[0], ts[0], Cc, Cr)

    Vol = np.zeros(len(ts))
    Vol[0] = mem.gamma(ts[0]) * I[0]

    # Shape: (100000, 1)
    # print('Voltage Shape: ', Vm.shape)

    # Update of the system
    for i in range(len(ts)-1):
        t = ts[i]

        Vol[i + 1] = mem.gamma(ts[i+1]) * I[i]

        # For now the potassium and sodium channels are not included in the update of the system

        k1 = qhh.k(t, eps, Zk[i], ZNa[i], ZL, Zout, I0[i], w[i], Cc, Cr, n0)
        q1 = qhh.q(t, eps, Zk[i], ZNa[i], ZL, Zout, I0[i], w[i], Cc, Cr, m0, h0)

        k2 = qhh.k(t + 0.5 * eps, eps, Zk[i] + 0.5 * k1, ZNa[i] + 0.5 * q1, ZL, Zout, I0[i], w[i], Cc, Cr, n0)
        q2 = qhh.q(t + 0.5 * eps, eps, Zk[i] + 0.5 * k1, ZNa[i] + 0.5 * q1, ZL, Zout, I0[i], w[i], Cc, Cr, m0, h0)

        k3 = qhh.k(t + 0.5 * eps, eps, Zk[i] + 0.5 * k2, ZNa[i] + 0.5 * q2, ZL, Zout, I0[i], w[i], Cc, Cr, n0)
        q3 = qhh.q(t + 0.5 * eps, eps, Zk[i] + 0.5 * k2, ZNa[i] + 0.5 * q2, ZL, Zout, I0[i], w[i], Cc, Cr, m0, h0)

        k4 = qhh.k(t + eps, eps, Zk[i] + k3, ZNa[i] + q3, ZL, Zout, I0[i], w[i], Cc, Cr, n0)
        q4 = qhh.q(t + eps, eps, Zk[i] + k3, ZNa[i] + q3, ZL, Zout, I0[i], w[i], Cc, Cr, m0, h0)

        # Update voltage of the potassium and sodium channels
        Zk[i + 1] = Zk[i] + (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        ZNa[i + 1] = ZNa[i] + (1 / 6) * (q1 + 2 * q2 + 2 * q3 + q4)

        # Update voltage of the system
        Vm[i + 1] = qhh.V(Zk[i + 1], ZNa[i + 1], ZL, Zout, I0[i], w[i], ts[i + 1], Cc, Cr)

    # Gk = 1.0 / Zk
    # GNa = 1.0 / ZNa

    plt.figure(figsize=(15, 8))

    plt.subplot(3, 2, 1)
    plt.plot(ts, I, 'b')
    plt.title("Input Current")
    plt.xlabel('Time')
    # plt.ylabel('Current <I>')

    plt.subplot(3, 2, 2)
    plt.plot(ts, Vol, 'r')
    plt.title("Voltage 1")
    plt.xlabel('Time')

    plt.subplot(3, 2, 3)
    plt.plot(ts, Vm, 'r')
    plt.title("Voltage 2")
    plt.xlabel('Time')

    plt.subplot(3, 2, 4)
    plt.plot(I, Vol, 'g')
    plt.xlabel('I')
    plt.ylabel('V')
    plt.title('Hysteresis Plot 1')

    plt.subplot(3, 2, 5)
    plt.plot(I, Vm, 'y')
    plt.xlabel('I')
    plt.ylabel('Vm')
    plt.title('Hysteresis Plot 2')

    plt.tight_layout()
    plt.savefig('HH_plot.png')

    plt.show()
