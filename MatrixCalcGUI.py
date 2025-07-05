import tkinter as tk
from tkinter import messagebox
import numpy as np

class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("3x3 Matrix Calculator")

        self.entries_A = []
        self.entries_B = []

        tk.Label(root, text="Matrix A").grid(row=0, column=0, columnspan=3)
        tk.Label(root, text="Matrix B").grid(row=0, column=4, columnspan=3)

        # Input fields for Matrix A and B
        for i in range(3):
            row_A = []
            row_B = []
            for j in range(3):
                e1 = tk.Entry(root, width=5)
                e1.grid(row=i+1, column=j)
                row_A.append(e1)

                e2 = tk.Entry(root, width=5)
                e2.grid(row=i+1, column=j+4)
                row_B.append(e2)

            self.entries_A.append(row_A)
            self.entries_B.append(row_B)

        # Buttons
        tk.Button(root, text="Calculate", command=self.calculate).grid(row=4, column=0, columnspan=7, pady=10)

        # Output Text
        self.output = tk.Text(root, width=80, height=25)
        self.output.grid(row=5, column=0, columnspan=7)

    def get_matrix(self, entries):
        matrix = []
        for row in entries:
            values = []
            for entry in row:
                try:
                    val = float(entry.get())
                except ValueError:
                    messagebox.showerror("Input Error", "All matrix fields must be numbers.")
                    return None
                values.append(val)
            matrix.append(values)
        return np.array(matrix, dtype=float)

    def calculate(self):
        A = self.get_matrix(self.entries_A)
        B = self.get_matrix(self.entries_B)

        if A is None or B is None:
            return

        output_text = ""

        try:
            output_text += f"Matrix A:\n{A}\n\n"
            output_text += f"Matrix B:\n{B}\n\n"

            output_text += f"A + B:\n{A + B}\n\n"
            output_text += f"A - B:\n{A - B}\n\n"
            output_text += f"A x B:\n{np.dot(A, B)}\n\n"

            det = np.linalg.det(A)
            output_text += f"Determinant of A: {round(det, 3)}\n"

            if det != 0:
                output_text += f"Inverse of A:\n{np.round(np.linalg.inv(A), 3)}\n\n"
            else:
                output_text += "Matrix A is singular, no inverse exists.\n\n"

            output_text += f"Transpose of A:\n{A.T}\n\n"
            output_text += f"Trace of A: {np.trace(A)}\n"
            output_text += f"Rank of A: {np.linalg.matrix_rank(A)}\n\n"

            eigenvalues, eigenvectors = np.linalg.eig(A)
            output_text += f"Eigenvalues of A:\n{np.round(eigenvalues, 3)}\n"
            output_text += f"Eigenvectors of A:\n{np.round(eigenvectors, 3)}\n\n"

            # Submatrices (minors)
            output_text += "Minors of A:\n"
            for i in range(3):
                for j in range(3):
                    minor = np.delete(np.delete(A, i, axis=0), j, axis=1)
                    output_text += f"Minor A[{i},{j}]:\n{minor}\n"
            output_text += "\n"

        except Exception as e:
            output_text += f"Error occurred: {e}"

        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, output_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculator(root)
    root.mainloop()
