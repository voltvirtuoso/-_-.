import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class BMI_Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        # Variables for user input
        self.weight_var = tk.DoubleVar()
        self.height_var = tk.DoubleVar()

        # Create SQLite database connection
        self.conn = sqlite3.connect("bmi_data.db")
        self.create_table()

        # Create GUI elements
        self.create_widgets()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Stylish Frame
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        frame = ttk.Frame(self.master, style="TFrame")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Labels and entry widgets for weight and height
        weight_label = ttk.Label(frame, text="Weight (kg):")
        weight_entry = ttk.Entry(frame, textvariable=self.weight_var)

        height_label = ttk.Label(frame, text="Height (m):")
        height_entry = ttk.Entry(frame, textvariable=self.height_var)

        # Calculate BMI button
        calculate_button = ttk.Button(frame, text="Calculate BMI", command=self.calculate_bmi)

        # Display BMI result
        self.result_label = ttk.Label(frame, text="BMI Result:")

        # BMI history button
        history_button = ttk.Button(frame, text="View History", command=self.view_history)

        # Layout
        weight_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        weight_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        height_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        height_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        history_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        # Make resizing behavior more responsive
        for i in range(5):
            frame.grid_rowconfigure(i, weight=1)
            frame.grid_columnconfigure(i, weight=1)

    def calculate_bmi(self):
        try:
            weight = self.weight_var.get()
            height = self.height_var.get()

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive values.")
                return

            bmi = weight / (height ** 2)
            category = self.classify_bmi(bmi)

            result_text = f"BMI: {bmi:.2f}\nCategory: {category}"
            self.result_label.config(text=result_text)

            # Store data
            self.store_data(weight, height, bmi, category)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def store_data(self, weight, height, bmi, category):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bmi_data (weight, height, bmi, category) VALUES (?, ?, ?, ?)
        ''', (weight, height, bmi, category))
        self.conn.commit()

    def view_history(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, weight, height, bmi, category FROM bmi_data ORDER BY timestamp DESC
        ''')
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("History", "No data available.")
            return

        # Create a new window for data visualization
        history_window = tk.Toplevel(self.master)
        history_window.title("BMI History")

        # Create a Matplotlib figure
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)

        # Extract data for visualization
        timestamps = [entry[0] for entry in data]
        weights = [entry[1] for entry in data]
        heights = [entry[2] for entry in data]
        bmis = [entry[3] for entry in data]

        # Plot BMI trends
        ax.plot(timestamps, bmis, marker='o', linestyle='-')
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("BMI")
        ax.set_title("BMI Trends Over Time")

        # Embed Matplotlib figure in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=history_window)
        canvas.get_tk_widget().pack()
        canvas.draw()


def main():
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
