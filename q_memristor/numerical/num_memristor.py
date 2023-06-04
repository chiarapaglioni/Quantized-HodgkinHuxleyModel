import numpy as np
from scipy.integrate import quad
from sympy import symbols, diff
from operators import *


class memristor:

    def __init__(self, y0, w, h, m, a, b):
        self.y0 = y0
        self.w = w
        self.h = h
        self.m = m
        self.a = a
        self.b = b

    # Note that --> gamma has a sinusoidal time dependance
    # Sinusoidal time dependence = quantity or phenomenon that varies with time in a sinusoidal/harmonic manner
    # Characterized by a periodic oscillation that follows a sine or cosine function.
    def gamma(self, ts):
        return self.y0 * (1 - np.sin(np.cos(self.w * ts)))

    def k(self, ts):
        # TODO: adapt implementation of k to include both timesteps instead of 0
        result, _ = quad(self.gamma, 0, ts)
        return -result / 2

    # Computes the density matrix of a system at time t
    # Implements Eq. 15 in "Quantum Memristors with Quantum Computers"
    def get_density_mat(self, k):
        mat = np.empty((2, 2), dtype='complex_')
        mat[0, 0] = (np.cos(self.a)*np.exp(k))**2
        mat[0, 1] = np.cos(self.a)*np.sin(self.a)*np.exp(-1j*self.b)*np.exp(k)
        mat[1, 0] = np.cos(self.a)*np.sin(self.a)*np.exp(1j*self.b)*np.exp(k)
        mat[1, 1] = 1-((np.cos(self.a)*np.exp(k))**2)
        return mat

    def exp_value(self, pauli_matrix, state_vector):
        """Compute the expectation value of a Pauli matrix.

        Args:
            pauli_matrix (str): The Pauli matrix to compute the expectation value for.
                                Can be 'X', 'Y', or 'Z'.
            state_vector (numpy.ndarray): The quantum state vector.

        Returns:
            float: The expectation value.
        """
        pauli_operator = pauli_matrix
        expectation = np.vdot(state_vector, pauli_operator @ state_vector)
        return expectation.real

    def derivative(self, func):
        # Define the variable
        t = symbols('t')
        # Define the function
        # func = t ** 2 + 3 * t + 1
        # Take the derivative with respect to t
        f_derivative = diff(func, t)
        print('Derviative: ', f_derivative)
        return f_derivative

    # Anticommutator --> {}
    def anticomm(self, matrix1, matrix2):
        return np.dot(matrix1, matrix2) + np.dot(matrix2, matrix1)

    # Commutator --> []
    def comm(self, matrix1, matrix2):
        return np.dot(matrix1, matrix2) - np.dot(matrix2, matrix1)

    # Implementation of Hamiltonian of the system
    # Eq. 5 in "Quantum Memristors with Quantum Computers"
    def hamiltonian(self):
        return (1/2)*self.h*self.w*(pauli_z2+2)

    # Implementation of master equation of the system
    # Eq. 10 in "Quantum Memristors with Quantum Computers"
    def master_eq_I(self, ts, p_I):
        return self.gamma(ts)*((np.dot(np.dot(pauli_low2, p_I), pauli_ris2))-(self.anticomm(np.dot(pauli_ris2, pauli_low2), p_I)))

    # Implementation of master equation of the system
    # Eq. 6 in "Quantum Memristors with Quantum Computers"
    def master_eq_2(self, ts, p_2):
        H = self.hamiltonian()
        return ((-1j/self.h)*self.comm(H, p_2))+self.gamma(ts)*((np.dot(np.dot(pauli_low2, p_2), pauli_ris2))-(self.anticomm(np.dot(pauli_ris2, pauli_low2), p_2)))

    def get_Schrödinger(self, t, p_I):
        # The function transforms the density matrix p_I at time t to the Schrödinger picture
        # i.e. it returns the corresponding p_2 at time t
        return np.exp((-1j*t)/(self.h*self.hamiltonian()))*p_I*np.exp((1j*t)/(self.h*self.hamiltonian()))


if __name__ == '__main__':
    # Time-steps
    eps = 0.1
    tmax = 100.1
    t = np.arange(0, tmax, eps)

    # Simulation parameters
    a = np.pi / 4
    b = np.pi / 5
    m = 1
    h = 1
    w = 1
    y0 = 0.4

    mem = memristor(y0, w, h, m, a, b)

    pure_state = np.array([np.cos(a), np.sin(a) * np.exp(1j * b)], dtype=complex)