from q_memristor.numerical.operators import *
from q_memristor.plots import iv_plot, time_plot
from num_memristor import memristor
import numpy as np

"""
    Dynamic Simulation of Single Quantum Memristor based on the article "Quantum Memristors with Quantum 
    Computers" from Y.-M. Guo, F. Albarr ́an-Arriagada, H. Alaeian, E. Solano, and G. Alvarado Barrios. 

    Author: Chiara Paglioni
    Link to Article: https://link.aps.org/doi/10.1103/PhysRevApplied.18.024082  
"""


if __name__ == '__main__':
    # Time-steps
    eps = 0.1
    tmax = 1.1
    t = np.arange(0, tmax, eps)

    # Simulation parameters
    a = np.pi / 4
    b = np.pi / 5
    m = 1
    h = 1
    w = 1
    y0 = 0.2
    amplitude = 1

    pauli_y = np.array([[0, -1j], [1j, 0]])
    pauli_x = np.array([[0, 1], [1, 0]])

    mem = memristor(y0, w, h, m, a, b)

    k = []
    density_states = []
    density_states2 = []
    schrodinger_states = []

    V = []
    I = []

    t_plt = time_plot.Tplot()

    for i in range(0, len(t)-1):
        k_val = mem.k1(t[i])

        if t[i] == 0.0:
            density_mat = mem.get_density_mat(k_val)
            schrodinger_mat = mem.get_Schrödinger(t[i], density_mat)
            density_states.append(density_mat)
            schrodinger_states.append(schrodinger_mat)

        else:
            density_mat = mem.get_E0(t[i], t[i+1]) @ density_states[0] @ mem.adjoint(mem.get_E0(t[i], t[i+1])) + mem.get_E1(t[i], t[i+1]) @ density_states[0] @ mem.adjoint(mem.get_E1(t[i], t[i+1]))
            schrodinger_mat = mem.get_Schrödinger(t[i], density_mat)
            density_states.append(density_mat)
            schrodinger_states.append(schrodinger_mat)

        k.append(k_val)

        print('Time: ', t[i])
        print('K: ', k_val)
        print('Density Matrix: ', '\n', density_mat)
        print('Schrodinger Picture: ', '\n', schrodinger_mat)

        exp_valueY = np.trace(pauli_y @ schrodinger_mat)
        exp_valueX = np.trace(pauli_x @ schrodinger_mat)

        print("Expectation value Y:", exp_valueY)
        print("Expectation value X:", exp_valueX)

        vol_val = -(1 / 2) * np.sqrt((m * h * w) / 2) * exp_valueY
        curr_val = np.sqrt((m * h * w) / 2) * exp_valueY - np.sqrt((m * w) / (2*h)) * exp_valueX
        curr_temp = mem.gamma(t[i]) * vol_val

        V.append(vol_val)
        I.append(curr_val)
        print('V: ', V[i], ' at time: ', t[i])
        print('I: ', I[i], ' at time: ', t[i])
        print('I: ', curr_temp, ' at time: ', t[i])
        print()

        t_plt.update(t[i], V[i], I[i])

    t_plt.save_plot()