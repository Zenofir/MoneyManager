import os
import sqlite3
import customtkinter as ctk
from tkinter import messagebox

from modules.setup_wizard import SetupWizard
from modules.Widget_AccountList import AccountListWidget
from modules.Widget_Transactions import TransactionListWidget
from modules.Widget_ExpenseChart import ExpenseChart
from modules.Widget_AccountBalanceChart import AccountBalanceChart

# Vérification de la base de données et exécution du setup si nécessaire
def check_and_initialize_database():
    if not os.path.exists("data/database.db"):
        return False
    return True

# Chargement du thème depuis la base SQLite
def load_theme_from_database():
    db_path = "data/database.db"
    if not os.path.exists(db_path):
        return "light"  # Thème par défaut

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT theme FROM user_preferences LIMIT 1")
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return "light"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mon Argent - Tableau de bord")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Barre de navigation
        self.navbar = ctk.CTkFrame(self, corner_radius=0)
        self.navbar.grid(row=0, column=0, sticky="nsw")
        self.navbar.grid_rowconfigure(5, weight=1)

        self.dashboard_button = ctk.CTkButton(self.navbar, text="Tableau de bord", command=self.show_dashboard)
        self.dashboard_button.grid(row=0, column=0, padx=10, pady=10)

        self.accounts_button = ctk.CTkButton(self.navbar, text="Comptes", command=self.show_accounts)
        self.accounts_button.grid(row=1, column=0, padx=10, pady=10)

        # Conteneur de page principale
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        # Widgets dynamiques
        self.dashboard_widgets = []
        self.show_dashboard()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()

        # Widget : Liste des comptes (haut gauche)
        account_list = AccountListWidget(self.main_frame)
        account_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Widget : Dernières opérations (sous liste des comptes)
        transactions = TransactionListWidget(self.main_frame)
        transactions.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Widget : Graphique dépenses par catégorie (droite haut)
        expense_chart = ExpenseChart(self.main_frame)
        expense_chart.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Widget : Graphique solde des comptes (droite bas)
        balance_chart = AccountBalanceChart(self.main_frame)
        balance_chart.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

    def show_accounts(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Gestion des comptes", font=("Arial", 18))
        label.pack(padx=20, pady=20)

if __name__ == "__main__":
    # Always create the CTk root before any widget
    app = ctk.CTk()
    # Initialisation de la base si nécessaire
    if not check_and_initialize_database():
        app.withdraw()  # cache la fenêtre principale
        SetupWizard()
        app.destroy()
        # Après le setup, relancer l'application principale
        app = ctk.CTk()
    # Application du thème
    ctk.set_appearance_mode(load_theme_from_database())
    ctk.set_default_color_theme("blue")

    main_app = MainApp()
    main_app.mainloop()


