import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3

class ExpenseChart(tk.Frame):
    def __init__(self, parent, db_path='data/database.db'):
        super().__init__(parent, bg="white", bd=1, relief="solid")
        self.db_path = db_path

        self.configure(padx=10, pady=10)

        self.label = tk.Label(self, text="Dépenses par catégorie", font=("Segoe UI", 12, "bold"), bg="white")
        self.label.pack(anchor="w")

        self.chart_frame = tk.Frame(self, bg="white")
        self.chart_frame.pack(fill="both", expand=True)

        self.create_chart()

    def create_chart(self):
        categories = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT category, amount FROM transactions WHERE amount < 0")
            for category, amount in cursor.fetchall():
                categories[category] = categories.get(category, 0) + abs(amount)
            conn.close()
        except sqlite3.Error as e:
            print("Erreur SQLite:", e)

        if not categories:
            categories = {"Aucune donnée": 1}

        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        ax.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=140)
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    widget = ExpenseChart(root)
    widget.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()
