"""
Nama  : Muharromi Ali Ilham
NIM   : F1D02410082
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from database.db_manager import DatabaseManager
from logic.controller import TransactionController
from ui.main_window import MainWindow

def load_stylesheet(app):
    style_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    with open(style_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    load_stylesheet(app)

    db_manager = DatabaseManager()
    controller = TransactionController(db_manager)
    window = MainWindow(controller)
    window.show()

    sys.exit(app.exec())
if __name__ == "__main__":
    main()