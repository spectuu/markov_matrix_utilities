# Markov Chains Calculator with GUI

This project is a Python graphical application for working with Markov chain transition matrices.  
It provides three main functionalities:

1. **Calculate steady-state vector**:  
   Solves the system \(\pi P = \pi\) with the normalization condition \(\sum \pi_i = 1\), displaying the solution.

example:
<src="images/Screenshot 2025-05-16 121913.png>


2. **Calculate state at time \(t\)**:  
   Given an initial vector \(\pi_0\), a transition matrix \(P\), and a time \(t\), computes \(\pi_t = \pi_0 P^t\).

example:
<src="images/Screenshot 2025-05-16 122029.png>
<src="images/Screenshot 2025-05-16 122046.png>
<src="images/Screenshot 2025-05-16 122059.png>

3. **Raise matrix \(P\) to power \(t\)**:  
   Raises the transition matrix \(P\) to the power \(t\) and shows the resulting matrix.

example:

<src="images/Screenshot 2025-05-16 122121.png">
<src="images/Screenshot 2025-05-16 122132.png">


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
