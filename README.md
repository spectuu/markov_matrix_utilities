# Markov Chains Calculator with GUI

This project is a Python graphical application for working with Markov chain transition matrices.  
It provides three main functionalities:

1. **Calculate steady-state vector**:  
   Solves the system \(\pi P = \pi\) with the normalization condition \(\sum \pi_i = 1\), displaying the solution.

2. **Calculate state at time \(t\)**:  
   Given an initial vector \(\pi_0\), a transition matrix \(P\), and a time \(t\), computes \(\pi_t = \pi_0 P^t\).
   
4. **Raise matrix \(P\) to power \(t\)**:  
   Raises the transition matrix \(P\) to the power \(t\) and shows the resulting matrix.

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
