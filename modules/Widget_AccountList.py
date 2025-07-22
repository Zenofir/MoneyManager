import sqlite3
import customtkinter as ctk
from tkinter import messagebox

class AccountListWidget(ctk.CTkFrame):
    def __init__(self, parent, full_view=False):
        super().__init__(parent)
        self.full_view = full_view
        self.configure(corner_radius=10)

        self.account_listbox = ctk.CTkScrollableFrame(self)
        self.account_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_accounts()

        if self.full_view:
            self.add_account_button = ctk.CTkButton(self, text="Ajouter un compte", command=self.add_account)
            self.add_account_button.pack(pady=10)

    def load_accounts(self):
        # Connexion à la base de données
        try:
            conn = sqlite3.connect("data/database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, balance FROM accounts")
            accounts = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur base de données", str(e))
            return

        # Affichage des comptes
        for widget in self.account_listbox.winfo_children():
            widget.destroy()

        if not accounts:
            no_account_label = ctk.CTkLabel(self.account_listbox, text="Aucun compte trouvé.")
            no_account_label.pack(pady=10)
            return

        for acc_id, name, balance in accounts:
            frame = ctk.CTkFrame(self.account_listbox)
            frame.pack(fill="x", padx=5, pady=5)

            name_label = ctk.CTkLabel(frame, text=name, font=("Arial", 14, "bold"))
            name_label.pack(side="left", padx=10)

            balance_label = ctk.CTkLabel(frame, text=f"{balance:.2f} €", font=("Arial", 14))
            balance_label.pack(side="right", padx=10)

    def add_account(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Nouveau compte")
        popup.geometry("300x200")

        name_entry = ctk.CTkEntry(popup, placeholder_text="Nom du compte")
        name_entry.pack(pady=10, padx=20)

        balance_entry = ctk.CTkEntry(popup, placeholder_text="Solde initial")
        balance_entry.pack(pady=10, padx=20)

        def save():
            name = name_entry.get()
            try:
                balance = float(balance_entry.get())
            except ValueError:
                messagebox.showerror("Erreur", "Le solde doit être un nombre.")
                return

            if not name:
                messagebox.showerror("Erreur", "Le nom du compte ne peut pas être vide.")
                return

            try:
                conn = sqlite3.connect("data/database.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
                conn.commit()
                conn.close()
            except sqlite3.Error as e:
                messagebox.showerror("Erreur base de données", str(e))
                return

            popup.destroy()
            self.load_accounts()

        save_button = ctk.CTkButton(popup, text="Ajouter", command=save)
        save_button.pack(pady=20)
