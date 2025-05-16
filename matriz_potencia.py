import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
import sympy as sp

class MarkovSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Cadenas de Markov")

        # Menú de selección
        self.mode_var = tk.StringVar(value="1")
        frame_mode = ttk.Frame(root)
        frame_mode.pack(padx=10, pady=5)

        ttk.Label(frame_mode, text="Selecciona la operación:").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_mode, text="1. Estado Estable", variable=self.mode_var, value="1").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_mode, text="2. Estado en Tiempo t", variable=self.mode_var, value="2").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(frame_mode, text="3. Elevar Matriz P a potencia t", variable=self.mode_var, value="3").pack(side=tk.LEFT, padx=5)

        # Área de entrada matriz
        self.label = ttk.Label(root, text="Ingrese matriz de transición (filas separadas por ;, valores por coma):")
        self.label.pack(padx=10, pady=5)

        self.matrix_entry = tk.Text(root, height=5, width=50)
        self.matrix_entry.insert(tk.END, "0.35,0.6,0.05;\n0.3,0.6,0.1;\n0.25,0.4,0.35")
        self.matrix_entry.pack(padx=10, pady=5)

        # Botón para ejecutar
        self.solve_button = ttk.Button(root, text="Ejecutar", command=self.execute)
        self.solve_button.pack(padx=10, pady=10)

        # Área de salida
        self.output = tk.Text(root, height=30, width=80, bg="white")
        self.output.pack(padx=10, pady=5)

    def execute(self):
        modo = self.mode_var.get()
        self.output.delete("1.0", tk.END)

        raw = self.matrix_entry.get("1.0", tk.END).strip()
        try:
            matrix = self.parse_matrix(raw)
            n = matrix.shape[0]
            if matrix.shape[0] != matrix.shape[1]:
                raise ValueError("La matriz debe ser cuadrada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer matriz: {e}")
            return

        if modo == "1":
            self.output.insert(tk.END, "Modo: Calcular vector de estado estable\n\n")
            self.calcular_estado_estable(matrix)
        elif modo == "2":
            self.output.insert(tk.END, "Modo: Calcular estado en tiempo t\n\n")
            self.calcular_estado_en_tiempo(matrix)
        elif modo == "3":
            self.output.insert(tk.END, "Modo: Elevar matriz P a potencia t\n\n")
            self.elevar_matriz_a_potencia(matrix)
        else:
            messagebox.showerror("Error", "Modo no reconocido")

    def calcular_estado_estable(self, matrix):
        n = matrix.shape[0]
        self.output.insert(tk.END, "Matriz de transición P:\n")
        self.output.insert(tk.END, np.array2string(matrix, formatter={'float_kind':lambda x: f"{x:.4f}"}))
        self.output.insert(tk.END, "\n\n")

        pi_syms = sp.symbols(f'π1:{n+1}')
        pi = sp.Matrix(pi_syms)
        P = sp.Matrix(matrix)

        self.output.insert(tk.END, "Planteamos el sistema π * P = π:\n")
        eqs = []
        for i in range(n):
            lhs = sum(pi[j]*P[j,i] for j in range(n))
            eq = sp.Eq(lhs, pi[i])
            eqs.append(eq)
            self.output.insert(tk.END, f"{sp.pretty(eq)}\n")
        self.output.insert(tk.END, "\n")

        self.output.insert(tk.END, "Reorganizamos a sistema homogéneo (π*P - π = 0):\n")
        homo_eqs = []
        for eq in eqs:
            lhs_homo = eq.lhs - eq.rhs
            homo_eqs.append(sp.Eq(lhs_homo, 0))
            self.output.insert(tk.END, f"{sp.pretty(sp.Eq(lhs_homo, 0))}\n")
        self.output.insert(tk.END, "\n")

        self.output.insert(tk.END, "Condición de normalización: π1 + π2 + ... + πn = 1\n\n")

        eqs_norm = homo_eqs[:-1]
        eqs_norm.append(sp.Eq(sum(pi_syms), 1))

        self.output.insert(tk.END, "Sistema para resolver:\n")
        for eq in eqs_norm:
            self.output.insert(tk.END, f"{sp.pretty(eq)}\n")

        self.output.insert(tk.END, "\nResolviendo sistema...\n")
        sol = sp.linsolve(eqs_norm, pi_syms)
        if not sol:
            self.output.insert(tk.END, "No se encontró solución.\n")
            return

        sol = list(sol)[0]
        self.output.insert(tk.END, "Solución:\n")
        for i, val in enumerate(sol):
            self.output.insert(tk.END, f"π{i+1} = {sp.N(val, 6)}\n")

        self.output.insert(tk.END, "\nVector estado estable π:\n[")
        self.output.insert(tk.END, ", ".join(f"{sp.N(v,6):.6f}" for v in sol))
        self.output.insert(tk.END, "]\n")

    def calcular_estado_en_tiempo(self, matrix):
        n = matrix.shape[0]
        self.output.insert(tk.END, "Matriz de transición P:\n")
        self.output.insert(tk.END, np.array2string(matrix, formatter={'float_kind':lambda x: f"{x:.4f}"}))
        self.output.insert(tk.END, "\n\n")

        vector_str = simpledialog.askstring("Vector inicial", f"Ingrese vector de estado inicial (n={n}, valores separados por comas):")
        if not vector_str:
            self.output.insert(tk.END, "No se ingresó vector inicial.\n")
            return
        try:
            pi0 = np.array([float(x.strip()) for x in vector_str.split(',')])
            if len(pi0) != n:
                raise ValueError(f"Vector inicial debe tener {n} elementos.")
            suma = np.sum(pi0)
            if abs(suma - 1) > 1e-6:
                self.output.insert(tk.END, f"Advertencia: vector inicial no suma 1 (suma={suma:.4f}). Se normalizará.\n")
                pi0 = pi0 / suma
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer vector inicial: {e}")
            return

        self.output.insert(tk.END, f"Vector inicial π0:\n{pi0}\n\n")

        t = simpledialog.askinteger("Tiempo t", "Ingrese el tiempo t (entero >=0):", minvalue=0)
        if t is None:
            self.output.insert(tk.END, "No se ingresó tiempo t.\n")
            return

        self.output.insert(tk.END, f"Tiempo t = {t}\n\n")

        Pt = np.linalg.matrix_power(matrix, t)
        self.output.insert(tk.END, f"Matriz P^{t}:\n")
        self.output.insert(tk.END, np.array2string(Pt, formatter={'float_kind':lambda x: f"{x:.6f}"}))
        self.output.insert(tk.END, "\n\n")

        pit = np.dot(pi0, Pt)
        self.output.insert(tk.END, f"Estado en tiempo t (π0 * P^{t}):\n")
        self.output.insert(tk.END, np.array2string(pit, formatter={'float_kind':lambda x: f"{x:.6f}"}))
        self.output.insert(tk.END, "\n")

    def elevar_matriz_a_potencia(self, matrix):
        n = matrix.shape[0]
        t = simpledialog.askinteger("Tiempo t", "Ingrese el tiempo t para elevar la matriz P^t (entero >=0):", minvalue=0)
        if t is None:
            self.output.insert(tk.END, "No se ingresó tiempo t.\n")
            return

        self.output.insert(tk.END, "Matriz de transición P:\n")
        self.output.insert(tk.END, np.array2string(matrix, formatter={'float_kind':lambda x: f"{x:.6f}"}))
        self.output.insert(tk.END, "\n\n")

        self.output.insert(tk.END, f"Matriz P^{t}:\n")
        Pt = np.linalg.matrix_power(matrix, t)
        self.output.insert(tk.END, np.array2string(Pt, formatter={'float_kind':lambda x: f"{x:.6f}"}))
        self.output.insert(tk.END, "\n")

    def parse_matrix(self, raw):
        rows = raw.split(';')
        matrix = []
        for r in rows:
            if r.strip():
                row_vals = [float(x.strip()) for x in r.strip().split(',')]
                matrix.append(row_vals)
        matrix = np.array(matrix)
        return matrix


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkovSolverApp(root)
    root.mainloop()