import os
import sqlite3
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox, QHBoxLayout, QScrollArea, QWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


def create_database(username: str, theme: str, comptes: list):
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect("db/database.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE utilisateur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            theme TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE compte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            solde_initial REAL NOT NULL
        );
    """)

    cursor.execute("INSERT INTO utilisateur (nom, theme) VALUES (?, ?);", (username, theme))

    for nom, solde in comptes:
        cursor.execute("INSERT INTO compte (nom, solde_initial) VALUES (?, ?);", (nom, solde))

    conn.commit()
    conn.close()


class SetupWizard(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration de départ")
        self.setMinimumSize(500, 600)

        self.layout = QVBoxLayout()

        title = QLabel("Bienvenue dans Mon Argent")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(title)

        subtitle = QLabel("Commençons par personnaliser votre expérience")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(20)
        self.layout.addWidget(QLabel("Quel est votre prénom ?"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Votre prénom")
        self.layout.addWidget(self.name_input)

        self.layout.addWidget(QLabel("Choisissez un thème :"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Light", "Dark"])
        self.theme_box.setEnabled(True)
        self.layout.addWidget(self.theme_box)

        self.layout.addSpacing(20)
        self.layout.addWidget(QLabel("Comptes à créer (au moins 1) :"))

        self.account_area = QVBoxLayout()
        self.account_widgets = []
        self.add_account_widget("Compte courant")

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.account_area)
        scroll = QScrollArea()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(250)
        self.layout.addWidget(scroll)

        self.add_button = QPushButton("➕ Ajouter un compte")
        self.add_button.clicked.connect(lambda: self.add_account_widget(""))
        self.layout.addWidget(self.add_button)

        self.submit_button = QPushButton("✅ Valider et créer la base")
        self.submit_button.clicked.connect(self.validate)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def add_account_widget(self, default_name):
        container = QHBoxLayout()
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nom du compte")
        name_input.setText(default_name)
        solde_input = QLineEdit()
        solde_input.setPlaceholderText("Solde initial")
        container.addWidget(name_input)
        container.addWidget(solde_input)
        self.account_area.addLayout(container)
        self.account_widgets.append((name_input, solde_input))

    def validate(self):
        username = self.name_input.text().strip()
        theme = self.theme_box.currentText()
        comptes = []

        if not username:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer votre prénom.")
            return

        valid_comptes = 0
        for name_edit, solde_edit in self.account_widgets:
            nom = name_edit.text().strip()
            solde_txt = solde_edit.text().strip()
            if nom and solde_txt:
                try:
                    solde = float(solde_txt)
                    comptes.append((nom, solde))
                    valid_comptes += 1
                except ValueError:
                    continue

        if valid_comptes == 0:
            QMessageBox.warning(self, "Erreur", "Vous devez créer au moins un compte avec un solde valide.")
            return

        create_database(username, theme, comptes)
        QMessageBox.information(self, "Succès", "Configuration terminée avec succès !")
        self.accept()


def run_initial_setup():
    # Remove QApplication, as CTk root is already created in Main.py
    wizard = SetupWizard()
    wizard.exec()
    del app
