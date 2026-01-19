import sys
from PyQt6.QtWidgets import QApplication
from app.views.main_window import MainWindow
from app.controllers.main_controller import MainController
from app.database import Database

def main():
    app = QApplication(sys.argv)
    
    # Initialize Database
    db = Database()
    db.init_db()

    # MVC Initialization
    window = MainWindow()
    controller = MainController(window) 
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
        