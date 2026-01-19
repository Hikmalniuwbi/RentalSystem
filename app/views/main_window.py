from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QListWidget, QStackedWidget, QLabel, QListWidgetItem,
    QFrame, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from app.views.inventory_view import InventoryView
from app.views.transaksi_view import TransaksiView  
from app.views.dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kelana Outdoor Rental System")
        self.setMinimumSize(1200, 850)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main Layout: Horizontal
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. SIDEBAR
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebar")
        self.sidebar_frame.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Branding
        brand_frame = QFrame()
        brand_frame.setObjectName("brand_frame")
        brand_frame.setFixedHeight(90)
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(25, 20, 25, 10)
        
        logo_label = QLabel("") 
        logo_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        
        self.brand_title = QLabel("KELANA OUTDOOR")
        self.brand_title.setStyleSheet("color: white; font-size: 18px; font-weight: 800; margin-top: -5px;")
        self.brand_subtitle = QLabel("RENTAL SYSTEM")
        self.brand_subtitle.setStyleSheet("color: #9ae6b4; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(self.brand_title)
        brand_layout.addWidget(self.brand_subtitle)
        
        sidebar_layout.addWidget(brand_frame)

        # Menu List
        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menu_list")
        
        self.add_menu_item("Dashboard", "")
        self.add_menu_item("Inventaris", "")
        self.add_menu_item("Transaksi", "")
        
        self.menu_list.setCurrentRow(0)
        sidebar_layout.addWidget(self.menu_list)
        
        sidebar_layout.addStretch()


        self.main_layout.addWidget(self.sidebar_frame)

        # 2. CONTENT AREA
        self.content_container = QFrame()
        self.content_container.setObjectName("content_container")
        self.right_layout = QVBoxLayout(self.content_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        # Top Header (Search & Profile)
        self.top_header = QFrame()
        self.top_header.setObjectName("top_header")
        self.top_header.setFixedHeight(70)
        header_layout = QHBoxLayout(self.top_header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        # Search Box
        self.search_box = QFrame()
        self.search_box.setObjectName("search_box")
        search_inner = QHBoxLayout(self.search_box)
        search_inner.setContentsMargins(15, 0, 15, 0)
        
        search_icon = QLabel("")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Quick Search (Ctrl+F)...")
        self.search_input.setObjectName("header_search")
        self.search_input.setStyleSheet("""
            QLineEdit#header_search {
                background: transparent;
                border: none;
                color: #2d3748;
                font-size: 13px;
            }
        """)
        
        search_inner.addWidget(search_icon)
        search_inner.addWidget(self.search_input)
        header_layout.addWidget(self.search_box)
        
        header_layout.addStretch()
        
        # User Profile Mockup
        profile_layout = QHBoxLayout()
        profile_layout.setSpacing(12)
        
        self.user_initials = QLabel("MA")
        self.user_initials.setObjectName("user_initials")
        self.user_initials.setFixedSize(36, 36)
        self.user_initials.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        user_info = QVBoxLayout()
        user_info.setSpacing(0)
        user_name = QLabel("Administrator")
        user_name.setObjectName("user_name")
        user_role = QLabel("Super Admin")
        user_role.setStyleSheet("color: #718096; font-size: 10px; font-weight: bold;")
        user_info.addWidget(user_name)
        user_info.addWidget(user_role)
        
        profile_layout.addLayout(user_info)
        profile_layout.addWidget(self.user_initials)
        
        header_layout.addLayout(profile_layout)
        


        # View Area (Stacked)
        self.tabs = QStackedWidget()
        
        self.dashboard_tab = DashboardView()
        self.inventory_tab = InventoryView()
        self.rental_tab = TransaksiView()
        
        self.tabs.addWidget(self.dashboard_tab)  # 0
        self.tabs.addWidget(self.inventory_tab)  # 1
        self.tabs.addWidget(self.rental_tab)     # 2
        
        self.right_layout.addWidget(self.tabs)
        
 
        
        self.main_layout.addWidget(self.content_container)

        # Connect Signals
        self.menu_list.currentRowChanged.connect(self.change_page)
        
        self.apply_styles()

    def add_menu_item(self, text, icon_char):
        item = QListWidgetItem(f" {text}")
        item.setSizeHint(QSize(240, 50))
        self.menu_list.addItem(item)

    def change_page(self, index):
        # Sidebar to stacked widget mapping
        # 0: Dashboard -> stack 0
        # 1: Inventory -> stack 1
        # 2: Transactions -> stack 2
        if index < 3:
            self.tabs.setCurrentIndex(index)

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f7fafc; }
            QWidget { font-family: 'Segoe UI', Roboto, sans-serif; }
            
            /* Sidebar */
            QFrame#sidebar {
                background-color: #22543d;
                border: none;
            }
            
            QFrame#brand_frame {
                border-bottom: 1px solid #276749;
            }
            
            QLabel#brand_label {
                color: #ffffff;
                font-size: 16px;
                font-weight: 700;
            }
            
            QListWidget#menu_list {
                background-color: transparent;
                border: none;
                margin-top: 20px;
                outline: none;
            }
            
            QListWidget#menu_list::item {
                color: #c6f6d5;
                padding-left: 10px;
                border-left: 4px solid transparent;
            }
            
            QListWidget#menu_list::item:selected {
                background-color: #2f855a;
                color: #ffffff;
                border-left: 4px solid #68d391;
                font-weight: bold;
            }
            
            QListWidget#menu_list::item:hover:!selected {
                background-color: #276749;
                color: #ffffff;
            }
            
            QLabel#sidebar_footer {
                color: #9ae6b4;
                padding: 15px;
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            
            /* Top Header */
            QFrame#top_header {
                background-color: #ffffff;
                border-bottom: 1px solid #edf2f7;
            }
            
            QFrame#search_box {
                background-color: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                min-width: 350px;
                max-height: 40px;
            }
            
            QLabel#user_initials {
                background-color: #22543d;
                color: white;
                border-radius: 18px; /* Circular */
                font-weight: bold;
                font-size: 11px;
            }
            
            QLabel#user_name {
                color: #2d3748;
                font-weight: 700;
                font-size: 13px;
            }
            
            /* Content Area */
            QStackedWidget {
                background-color: #f7fafc;
                padding: 30px;
            }
            
            QFrame#status_bar {
                background-color: #ffffff;
                border-top: 1px solid #edf2f7;
            }
        """)
