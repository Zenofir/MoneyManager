import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3

class AccountBalanceChart(tk.Frame):
    def __init__(self, parent, db_path='data/database.db'):
        super().__init__(parent, bg="white", bd=1, relief="solid")
        self.db_path = db_path

        self.configure(padx=10, pady=10)

        self.label = tk.Label(self, text="Solde des Comptes", font=("Segoe UI", 12, "bold"), bg="white")
        self.label.pack(anchor="w")

        self.chart_frame = tk.Frame(self, bg="white")
        self.chart_frame.pack(fill="both", expand=True)

        self.create_chart()

    def create_chart(self):
        accounts = []
        balances = []

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name, balance FROM accounts")
            results = cursor.fetchall()
            for name, balance in results:
                accounts.append(name)
                balances.append(balance)
            conn.close()
        except sqlite3.Error as e:
            print("Erreur SQLite:", e)

        if not accounts:
            accounts = ["Aucun"]
            balances = [0]

        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        bars = ax.bar(accounts, balances, color="#4a90e2")
        ax.set_ylabel("Solde (€)")
        ax.set_title("Solde actuel par compte")
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval:.2f}", ha='center', va='bottom', fontsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    widget = AccountBalanceChart(root)
    widget.pack(fill="both", expand=True, padx=10, pady=10)
    root.mainloop()
