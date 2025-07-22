import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime


class TransactionListWidget(ctk.CTkFrame):
    def __init__(self, master, full_view=False, **kwargs):
        super().__init__(master, **kwargs)
        self.full_view = full_view
        self.transactions = []

        self.build_ui()
        self.load_transactions()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Transactions", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(padx=10, pady=(10, 5), anchor="w")

        self.transaction_listbox = ctk.CTkScrollableFrame(self)
        self.transaction_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        if self.full_view:
            add_button = ctk.CTkButton(self, text="Ajouter une transaction", command=self.add_transaction_popup)
            add_button.pack(pady=10)

    def load_transactions(self):
        try:
            conn = sqlite3.connect("data/database.db")
            cursor = conn.cursor()

            query = """
                SELECT t.date, a.name, t.description, t.amount
                FROM transactions t
                JOIN accounts a ON t.account_id = a.id
                ORDER BY t.date DESC
                LIMIT ?
            """
            limit = 50 if self.full_view else 5
            cursor.execute(query, (limit,))
            self.transactions = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les transactions.\n{e}")
            return

        # Nettoyage de la liste affichée
        for widget in self.transaction_listbox.winfo_children():
            widget.destroy()

        for transaction in self.transactions:
            date_str, account_name, description, amount = transaction
            row = ctk.CTkFrame(self.transaction_listbox)
            row.pack(fill="x", padx=5, pady=2)

            date_label = ctk.CTkLabel(row, text=date_str, width=90)
            date_label.pack(side="left", padx=5)

            desc_label = ctk.CTkLabel(row, text=description, anchor="w")
            desc_label.pack(side="left", padx=5, fill="x", expand=True)

            account_label = ctk.CTkLabel(row, text=account_name, width=120)
            account_label.pack(side="left", padx=5)

            amount_label = ctk.CTkLabel(row, text=f"{amount:.2f} €", text_color="green" if amount >= 0 else "red")
            amount_label.pack(side="right", padx=5)

    def add_transaction_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Nouvelle transaction")
        popup.geometry("350x350")
        popup.grab_set()

        # Champs
        ctk.CTkLabel(popup, text="Compte :").pack(pady=(15, 0))
        account_dropdown = ctk.CTkComboBox(popup, values=self.get_account_names())
        account_dropdown.pack(pady=5)

        ctk.CTkLabel(popup, text="Description :").pack(pady=(10, 0))
        desc_entry = ctk.CTkEntry(popup)
        desc_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Montant (€) :").pack(pady=(10, 0))
        amount_entry = ctk.CTkEntry(popup)
        amount_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Date (YYYY-MM-DD) :").pack(pady=(10, 0))
        date_entry = ctk.CTkEntry(popup)
        date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        date_entry.pack(pady=5)

        def save_transaction():
            account_name = account_dropdown.get()
            description = desc_entry.get().strip()
            try:
                amount = float(amount_entry.get().replace(",", "."))
            except ValueError:
                messagebox.showerror("Erreur", "Le montant est invalide.")
                return

            try:
                datetime.strptime(date_entry.get(), "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Erreur", "Format de date invalide (YYYY-MM-DD).")
                return

            try:
                conn = sqlite3.connect("data/database.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM accounts WHERE name = ?", (account_name,))
                result = cursor.fetchone()
                if not result:
                    raise Exception("Compte non trouvé.")
                account_id = result[0]

                cursor.execute(
                    "INSERT INTO transactions (account_id, description, amount, date) VALUES (?, ?, ?, ?)",
                    (account_id, description, amount, date_entry.get())
                )
                conn.commit()
                conn.close()
                popup.destroy()
                self.load_transactions()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ajouter la transaction.\n{e}")

        save_btn = ctk.CTkButton(popup, text="Ajouter", command=save_transaction)
        save_btn.pack(pady=20)

    def get_account_names(self):
        try:
            conn = sqlite3.connect("data/database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM accounts ORDER BY name")
            rows = cursor.fetchall()
            conn.close()
            return [r[0] for r in rows]
        except:
            return []
