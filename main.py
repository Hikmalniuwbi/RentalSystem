import sys
from PyQt6.QtWidgets import QApplication
from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController
from app.database import Database

def main():
    app = QApplication(sys.argv)
    
    # Inisialisasi Database
    db = Database()
    db.init_db()

    # Inisialisasi MVC
    window = MainWindow()
    controller = MainController(window) 
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
        