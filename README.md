# Markov Chains Calculator with GUI

This project is a Python graphical application for working with Markov chain transition matrices.  
It provides three main functionalities:

1. **Calculate steady-state vector**:  
   Solves the system \(\pi P = \pi\) with the normalization condition \(\sum \pi_i = 1\), displaying the solution.

Example:  
![Steady state example](images/Screenshot_2025-05-16_121913.png)


2. **Calculate state at time \(t\)**:  
   Given an initial vector \(\pi_0\), a transition matrix \(P\), and a time \(t\), computes \(\pi_t = \pi_0 P^t\).

Example:  
![State at time 1](/images/Screenshot_2025-05-16_122029.png)  
![State at time 2](images/Screenshot_2025-05-16_122046.png)  
![State at time 3](images/Screenshot_2025-05-16_122059.png)

3. **Raise matrix \(P\) to power \(t\)**:  
   Raises the transition matrix \(P\) to the power \(t\) and shows the resulting matrix.

Example:  
![Matrix power 1](images/Screenshot_2025-05-16_122121.png)  
![Matrix power 2](images/Screenshot_2025-05-16_122132.png)

---

## Requirements

- Python 3.8 or higher
- Libraries:  
  - numpy  
  - sympy  
  - tkinter (usually included with Python)

Install the necessary packages with:

```bash
pip install numpy sympy
