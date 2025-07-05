import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MatrixVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3x3 Matrix Visual Calculator")

        self.entries_A = []
        self.entries_B = []

        tk.Label(root, text="Matrix A").grid(row=0, column=0, columnspan=3)
        tk.Label(root, text="Matrix B").grid(row=0, column=4, columnspan=3)

        for i in range(3):
            row_A, row_B = [], []
            for j in range(3):
                e1 = tk.Entry(root, width=5)
                e1.grid(row=i+1, column=j)
                row_A.append(e1)

                e2 = tk.Entry(root, width=5)
                e2.grid(row=i+1, column=j+4)
                row_B.append(e2)

            self.entries_A.append(row_A)
            self.entries_B.append(row_B)

        tk.Button(root, text="Calculate & Visualize", command=self.calculate).grid(row=4, column=0, columnspan=7, pady=10)

        self.text_output = tk.Text(root, width=75, height=10)
        self.text_output.grid(row=5, column=0, columnspan=7)

        # Placeholder for matplotlib canvas
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.grid(row=6, column=0, columnspan=7)

    def get_matrix(self, entries):
        matrix = []
        for row in entries:
            values = []
            for entry in row:
                try:
                    val = float(entry.get())
                except ValueError:
                    messagebox.showerror("Input Error", "All fields must be numbers.")
                    return None
                values.append(val)
            matrix.append(values)
        return np.array(matrix)

    def visualize_matrix(self, matrix, title, subplot, fig):
        ax = fig.add_subplot(subplot)
        ax.matshow(matrix, cmap="coolwarm")
        for i in range(3):
            for j in range(3):
                ax.text(j, i, f"{matrix[i][j]:.1f}", va='center', ha='center', color='black')
        ax.set_title(title)

    def calculate(self):
        A = self.get_matrix(self.entries_A)
        B = self.get_matrix(self.entries_B)
        if A is None or B is None:
            return

        output = ""
        self.text_output.delete(1.0, tk.END)

        fig = plt.Figure(figsize=(10, 4))
        self.canvas_frame.destroy()  # remove old canvas
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=6, column=0, columnspan=7)

        try:
            sum_matrix = A + B
            diff_matrix = A - B
            mult_matrix = A @ B
            det = round(np.linalg.det(A), 3)

            output += f"Determinant of A: {det}\n"
            output += f"Trace of A: {np.trace(A)}\n"
            output += f"Rank of A: {np.linalg.matrix_rank(A)}\n"

            if det != 0:
                inv_matrix = np.linalg.inv(A)
                output += "Inverse exists.\n"
            else:
                inv_matrix = None
                output += "Matrix A is singular. Inverse not available.\n"

            self.visualize_matrix(A, "Matrix A", 231, fig)
            self.visualize_matrix(B, "Matrix B", 232, fig)
            self.visualize_matrix(sum_matrix, "A + B", 233, fig)
            self.visualize_matrix(diff_matrix, "A - B", 234, fig)
            self.visualize_matrix(mult_matrix, "A × B", 235, fig)

            if inv_matrix is not None:
                self.visualize_matrix(inv_matrix, "Inverse of A", 236, fig)

        except Exception as e:
            output += f"\nError: {e}"

        self.text_output.insert(tk.END, output)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixVisualizerApp(root)
    root.mainloop()
