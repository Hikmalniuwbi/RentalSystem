from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QListWidget, QStackedWidget, QLabel, QListWidgetItem,
    QFrame, QLineEdit
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import os
from app.views.inventory_view import InventoryView
from app.views.transaksi_view import TransaksiView  
from app.views.dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kelana Outdoor Rental System")
        
        # Set Window Icon
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icon_path = os.path.join(base_dir, "Kelana.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(1200, 850)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout Utama: Horizontal
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. PANEL SAMPING
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebar")
        self.sidebar_frame.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Branding (Merek)
        # Branding (Merek)
        brand_frame = QFrame()
        brand_frame.setObjectName("brand_frame")
        brand_frame.setFixedHeight(180)  # Diperbesar LAGI agar logo 100% muat dan tidak terpotong
        brand_layout = QVBoxLayout(brand_frame)
        brand_layout.setContentsMargins(20, 20, 20, 10)
        
        logo_label = QLabel()
        # Mencari path gambar Kelana.png relatif terhadap file ini
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(base_dir, "Kelana.png")
        
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Scaling proporsional: Maksimum lebar 180px (sidebar 240 - margin), tinggi 60px
            scaled_pixmap = pixmap.scaled(QSize(180, 80), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Tengah secara horizontal
            logo_label.setContentsMargins(0, 0, 0, 15)
        else:
            logo_label.setText("KELANA")
            logo_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        self.brand_title = QLabel("KELANA OUTDOOR")
        self.brand_title.setStyleSheet("color: white; font-size: 18px; font-weight: 800; margin-top: -5px;")
        self.brand_subtitle = QLabel("RENTAL SYSTEM")
        self.brand_subtitle.setStyleSheet("color: #9ae6b4; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(self.brand_title)
        brand_layout.addWidget(self.brand_subtitle)
        
        sidebar_layout.addWidget(brand_frame)

        # Daftar Menu
        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menu_list")
        
        self.add_menu_item("Dashboard", "")
        self.add_menu_item("Inventaris", "")
        self.add_menu_item("Transaksi", "")
        
        self.menu_list.setCurrentRow(0)
        sidebar_layout.addWidget(self.menu_list)
        
        sidebar_layout.addStretch()


        self.main_layout.addWidget(self.sidebar_frame)

        # 2. AREA KONTEN
        self.content_container = QFrame()
        self.content_container.setObjectName("content_container")
        self.right_layout = QVBoxLayout(self.content_container)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(0)

        # Header Atas (Pencarian & Profil)
        self.top_header = QFrame()
        self.top_header.setObjectName("top_header")
        self.top_header.setFixedHeight(70)
        header_layout = QHBoxLayout(self.top_header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        # Kotak Pencarian
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
        
        # Mockup Profil Pengguna
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
        


        # Area Tampilan (Stacked)
        self.tabs = QStackedWidget()
        
        self.dashboard_tab = DashboardView()
        self.inventory_tab = InventoryView()
        self.rental_tab = TransaksiView()
        
        self.tabs.addWidget(self.dashboard_tab)  # 0
        self.tabs.addWidget(self.inventory_tab)  # 1
        self.tabs.addWidget(self.rental_tab)     # 2
        
        self.right_layout.addWidget(self.tabs)
        
 
        
        self.main_layout.addWidget(self.content_container)

        # Hubungkan Sinyal
        self.menu_list.currentRowChanged.connect(self.change_page)
        
        self.apply_styles()

    def add_menu_item(self, text, icon_char):
        item = QListWidgetItem(f" {text}")
        item.setSizeHint(QSize(240, 50))
        self.menu_list.addItem(item)

    def change_page(self, index):
        # Pemetaan Sidebar ke Stacked Widget
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
