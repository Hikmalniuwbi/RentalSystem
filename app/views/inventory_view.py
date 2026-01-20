from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, 
    QFrame, QProgressBar, QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt, QSize

class InventoryView(QWidget):
    def __init__(self):
        """
        [MVC - View]
        Inisialisasi tampilan manajemen inventaris.
        """
        super().__init__()
        self.init_ui()
        self.apply_view_styles()

    def init_ui(self):
        """
        [MVC - View]
        Membangun struktur visual (Layout, Tombol, Tabel).
        View hanya mendefinisikan 'apa yang dilihat user', tanpa logika bisnis.
        """
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # Baris Atas
        top_bar = QFrame()
        top_bar.setFixedHeight(60)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setFixedSize(80, 40)
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari Instant...")
        self.search_input.setFixedHeight(40)
        self.search_input.setMinimumWidth(300)

        self.cat_filter = QComboBox()
        self.cat_filter.addItem("Semua Kategori")
        self.cat_filter.setFixedHeight(40)
        self.cat_filter.setMinimumWidth(150)

        self.btn_add = QPushButton("+ Tambah Barang")
        self.btn_add.setFixedHeight(40)
        self.btn_add.setObjectName("primary_btn")
        self.btn_add.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_set_price = QPushButton("+ Paket Harga")
        self.btn_set_price.setFixedHeight(40)
        self.btn_set_price.setObjectName("secondary_btn")
        self.btn_set_price.setCursor(Qt.CursorShape.PointingHandCursor)

        top_bar_layout.addWidget(self.btn_refresh)
        top_bar_layout.addWidget(self.search_input)
        top_bar_layout.addWidget(self.cat_filter)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.btn_set_price)
        top_bar_layout.addWidget(self.btn_add)

        self.main_layout.addWidget(top_bar)

        # Tabel Inventaris (Daftar)
        self.table = QTableWidget()
        self.table.setColumnCount(7) 
        self.table.setHorizontalHeaderLabels(["ID", "NAMA ITEM", "KATEGORI", "SKU", "Ketersediaan", "STOK ", "ACTION"])
        self.table.setColumnHidden(0, True) 
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(6, 180)
        
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.main_layout.addWidget(self.table)

    def apply_view_styles(self):
        """
        [MVC - View]
        Menerapkan styling CSS untuk mempercantik tampilan.
        """
        self.setStyleSheet("""
            QWidget#InventoryView { background-color: #f7fafc; }
            QLineEdit {
                background-color: white; border: 1px solid #e2e8f0; border-radius: 8px;
                padding: 0 15px; color: #2d3748;
            }
            QComboBox {
                background-color: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0 15px;
            }
            QPushButton#primary_btn {
                background-color: #22543d; color: white; border-radius: 8px; padding: 0 20px; font-weight: bold;
            }
            QPushButton#secondary_btn {
                background-color: white; border: 1px solid #e2e8f0; border-radius: 8px;
                padding: 0 20px; font-weight: bold; color: #4a5568;
            }
            QTableWidget {
                background-color: white; border: 1px solid #e2e8f0; border-radius: 12px;
                alternate-background-color: #f8fafc; selection-background-color: #f0fdf4;
                selection-color: #22543d; outline: none;
            }
            QTableWidget::item { padding: 8px; color: #2d3748; font-size: 13px; }
            QHeaderView::section {
                background-color: #f8fafc; color: #4a5568; padding: 8px 10px; border: none;
                border-bottom: 2px solid #edf2f7; font-weight: 700; font-size: 11px;
                text-transform: uppercase; letter-spacing: 0.5px;
            }
            QProgressBar {
                background-color: #edf2f7; border-radius: 4px; text-align: center; border: none; height: 8px;
            }
            QProgressBar::chunk { border-radius: 4px; }
            QPushButton#card_btn {
                background-color: white; border: 1px solid #cbd5e0; border-radius: 6px;
                font-size: 11px; font-weight: 700; color: #2b6cb0; padding: 6px 12px;
            }
            QPushButton#delete_btn {
                background-color: white; border: 1px solid #fed7d7; border-radius: 6px;
                font-size: 11px; font-weight: 700; color: #e53e3e; padding: 6px 12px;
            }
        """)

    def display_items(self, items):
        """
        [MVC - View]
        Menampilkan data barang ke dalam tabel.
        Menerima list dictionary 'items' dari Controller dan merender baris demi baris.
        Juga memperbarui pilihan filter kategori secara dinamis.
        """
        self.table.setRowCount(len(items))
        
        kategori_set = sorted(list(set(item['kategori'] for item in items)))
        kat_sekarang = self.cat_filter.currentText()
        self.cat_filter.blockSignals(True)
        self.cat_filter.clear()
        self.cat_filter.addItem("Semua Kategori")
        self.cat_filter.addItems(kategori_set)
        self.cat_filter.setCurrentText(kat_sekarang)
        self.cat_filter.blockSignals(False)

        for baris, item in enumerate(items):
            self.table.setItem(baris, 0, QTableWidgetItem(item['id']))
            
            nama_item = QTableWidgetItem(item['nama'])
            nama_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(baris, 1, nama_item)
            
            kat_item = QTableWidgetItem(item['kategori'])
            kat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(baris, 2, kat_item)
            
            sku = f"{item['kategori'][:3].upper()}-{item['id'][:8].upper()}"
            sku_item = QTableWidgetItem(sku)
            sku_item.setForeground(Qt.GlobalColor.gray)
            sku_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(baris, 3, sku_item)
            
            tersedia = item.get('stok_tersedia', 0)
            total = item['stok_total']
            persen = int((tersedia / total * 100)) if total > 0 else 0
            
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(10, 0, 10, 0)
            
            teks_badge = "TERSEDIA"
            warna_badge = "#38a169"
            if persen < 30:
                teks_badge = "HAMPIR HABIS"
                warna_badge = "#e53e3e"
            elif persen == 0:
                teks_badge = "STOK HABIS"
                warna_badge = "#718096"

            badge = QLabel(teks_badge)
            badge.setStyleSheet(f"background-color: {warna_badge}1a; color: {warna_badge}; border: 1px solid {warna_badge}33; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 800;")
            status_layout.addWidget(badge)
            status_layout.addStretch()
            self.table.setCellWidget(baris, 4, status_widget)
            
            progress_container = QWidget()
            progress_layout = QVBoxLayout(progress_container)
            progress_layout.setContentsMargins(10, 10, 10, 10)
            
            pbar = QProgressBar()
            pbar.setFixedHeight(8)
            pbar.setRange(0, 100)
            pbar.setValue(persen)
            pbar.setTextVisible(False)
            
            warna_pbar = "#38a169" if persen > 60 else ("#ecc94b" if persen > 30 else "#e53e3e")
            pbar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {warna_pbar}; }}")
            
            label_pbar = QLabel(f"{tersedia} / {total} Unit")
            label_pbar.setStyleSheet("font-size: 10px; color: #718096; font-weight: bold;")
            
            progress_layout.addWidget(pbar)
            progress_layout.addWidget(label_pbar)
            self.table.setCellWidget(baris, 5, progress_container)
            
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(10, 5, 10, 5)
            action_layout.setSpacing(8)
            
            id_brg = item['id']
            nama_brg = item['nama']
            
            btn_manage = QPushButton("Kelola")
            btn_manage.setObjectName("card_btn")
            btn_manage.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_manage.clicked.connect(lambda _, i=id_brg, n=nama_brg: self.request_manage_item(i, n))
            
            btn_delete = QPushButton("Hapus")
            btn_delete.setObjectName("delete_btn")
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_delete.clicked.connect(lambda _, i=id_brg, n=nama_brg: self.request_delete_item(i, n))
            
            action_layout.addStretch()
            action_layout.addWidget(btn_manage)
            action_layout.addWidget(btn_delete)
            action_layout.addStretch()
            self.table.setCellWidget(baris, 6, action_widget)
            
            self.table.setRowHeight(baris, 65)

    def show_context_menu(self, pos):
        """
        [MVC - View]
        Menampilkan menu klik kanan (Context Menu) pada baris tabel.
        Mengirim sinyal permintaan aksi ke Controller saat menu dipilih.
        """
        row = self.table.currentRow()
        if row < 0: return
        id_brg, nama_brg = self.get_item_by_row(row)
        
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        manage_action = menu.addAction("Kelola Item")
        delete_action = menu.addAction("Hapus Item")
        delete_action.setStyleSheet("color: #e53e3e;")
        
        action = menu.exec(self.table.mapToGlobal(pos))
        if action == manage_action:
            self.request_manage_item(id_brg, nama_brg)
        elif action == delete_action:
            self.request_delete_item(id_brg, nama_brg)

    def get_selected_item(self):
        """
        [MVC - View]
        Helper untuk mendapatkan ID dan Nama barang yang sedang dipilih user.
        Digunakan oleh Controller untuk mengetahui barang mana yang akan diedit.
        """
        row = self.table.currentRow()
        if row >= 0:
            return self.table.item(row, 0).text(), self.table.item(row, 1).text()
        return None

    def get_item_by_row(self, row):
        if 0 <= row < self.table.rowCount():
            return self.table.item(row, 0).text(), self.table.item(row, 1).text()
        return None
