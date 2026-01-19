from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QTableWidgetItem, 
    QPushButton, QDialog, QSpinBox, QVBoxLayout, QTableWidget,
    QHeaderView, QLabel, QFrame, QLineEdit, QDateEdit, QGroupBox,
    QScrollArea, QGridLayout
)
from PyQt6.QtCore import QDate, Qt

class TransaksiView(QWidget):
    def __init__(self):
        super().__init__()
        self.cart = []
        self.status_map = {
            'BOOKED': 'BOOKING',
            'ACTIVE': 'AKTIF',
            'RETURNED': 'DIKEMBALIKAN',
            'CANCELLED': 'DIBATALKAN'
        }
        self.reverse_status_map = {v: k for k, v in self.status_map.items()}
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setContentsMargins(30, 30, 30, 30)
        self.scroll_layout.setSpacing(30)
        scroll.setWidget(scroll_content)
        self.main_layout.addWidget(scroll)

        trans_header_row = QHBoxLayout()
        title = QLabel("HISTORI TRANSAKSI")
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: #1a202c;")
        
        self.search_trans = QLineEdit()
        self.search_trans.setPlaceholderText("Filter history...")
        self.search_trans.setFixedWidth(250)
        self.search_trans.setFixedHeight(35)
        
        self.btn_refresh_dashboard = QPushButton("Refresh")
        self.btn_refresh_dashboard.setFixedWidth(100)
        self.btn_refresh_dashboard.setFixedHeight(35)
        self.btn_refresh_dashboard.setObjectName("secondary_btn")
        
        trans_header_row.addWidget(title)
        trans_header_row.addStretch()
        trans_header_row.addWidget(self.search_trans)
        trans_header_row.addWidget(self.btn_refresh_dashboard)
        self.scroll_layout.addLayout(trans_header_row)

        self.trans_table = QTableWidget()
        self.trans_table.setColumnCount(6)
        self.trans_table.setHorizontalHeaderLabels(["TANGGAL", "ID TRANSAKSI", "NAMA PELANGGAN", "STATUS", "ITEM", "TOTAL BIAYA"])
        self.trans_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.trans_table.verticalHeader().setVisible(False)
        self.trans_table.setMinimumHeight(250)
        self.trans_table.setObjectName("modern_table")
        self.scroll_layout.addWidget(self.trans_table)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #e2e8f0;")
        self.scroll_layout.addWidget(line)

        create_title = QLabel("BUAT TRANSAKSI BARU")
        create_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #1a202c;")
        self.scroll_layout.addWidget(create_title)

        main_creation_content = QHBoxLayout()
        main_creation_content.setSpacing(25)

        left_side = QVBoxLayout()
        left_side.setSpacing(20)

        form_card = QFrame()
        form_card.setObjectName("white_card")
        form_layout = QVBoxLayout(form_card)
        form_layout.setSpacing(15)

        row1 = QHBoxLayout()
        v_name = QVBoxLayout()
        v_name.addWidget(QLabel("NAMA PELANGGAN"))
        self.inp_name = QLineEdit(); self.inp_name.setPlaceholderText("Nama Pelanggan...")
        v_name.addWidget(self.inp_name); row1.addLayout(v_name)

        v_contact = QVBoxLayout()
        v_contact.addWidget(QLabel("NO. KONTAK"))
        self.inp_contact = QLineEdit(); self.inp_contact.setPlaceholderText("No. Kontak...")
        v_contact.addWidget(self.inp_contact); row1.addLayout(v_contact)
        form_layout.addLayout(row1)

        row2 = QHBoxLayout()
        v_start = QVBoxLayout()
        v_start.addWidget(QLabel("TANGGAL SEWA"))
        self.inp_start_date = QDateEdit(); self.inp_start_date.setCalendarPopup(True)
        self.inp_start_date.setDate(QDate.currentDate())
        v_start.addWidget(self.inp_start_date); row2.addLayout(v_start)

        v_end = QVBoxLayout()
        v_end.addWidget(QLabel("TANGGAL KEMBALI"))
        self.inp_end_date = QDateEdit(); self.inp_end_date.setCalendarPopup(True)
        self.inp_end_date.setDate(QDate.currentDate().addDays(3))
        v_end.addWidget(self.inp_end_date); row2.addLayout(v_end)
        form_layout.addLayout(row2)

        left_side.addWidget(form_card)

        item_card = QFrame()
        item_card.setObjectName("white_card")
        item_layout = QVBoxLayout(item_card)
        
        item_sel_header = QHBoxLayout()
        item_sel_header.addWidget(QLabel("BARANG TERSEDIA"))
        item_sel_header.addStretch()
        self.search_item = QLineEdit(); self.search_item.setPlaceholderText("Cari barang...")
        item_sel_header.addWidget(self.search_item)
        item_layout.addLayout(item_sel_header)

        self.avail_table = QTableWidget()
        self.avail_table.setColumnCount(3)
        self.avail_table.setHorizontalHeaderLabels(["NAMA BARANG", "STOK", "AKSI"])
        header = self.avail_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.avail_table.setMinimumHeight(200)
        item_layout.addWidget(self.avail_table)
        
        left_side.addWidget(item_card)
        main_creation_content.addLayout(left_side, 2)

        right_side = QVBoxLayout()
        right_side.setSpacing(20)

        cart_card = QFrame()
        cart_card.setObjectName("white_card")
        cart_layout = QVBoxLayout(cart_card)
        cart_layout.addWidget(QLabel("KERANJANG (CART)"))
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(["ITEM", "JUMLAH", "SUBTOTAL", ""])
        self.cart_table.setMinimumHeight(200)
        
        c_header = self.cart_table.horizontalHeader()
        c_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        c_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        c_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        c_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.cart_table.setColumnWidth(3, 40)
        
        cart_layout.addWidget(self.cart_table)
        right_side.addWidget(cart_card)

        self.summary_card = QFrame()
        self.summary_card.setObjectName("summary_card")
        summary_layout = QVBoxLayout(self.summary_card)
        summary_layout.setContentsMargins(25, 25, 25, 25)
        
        sum_header = QHBoxLayout()
        sum_header.addWidget(QLabel("TOTAL BIAYA"))
        sum_header.addStretch()
        sum_header.addWidget(QLabel(""))
        summary_layout.addLayout(sum_header)
        
        self.lbl_total_big = QLabel("Rp 0")
        self.lbl_total_big.setObjectName("total_big")
        summary_layout.addWidget(self.lbl_total_big, 0, Qt.AlignmentFlag.AlignCenter)
        
        summary_layout.addSpacing(15)
        
        def add_sum_row(label, val_attr):
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            label_val = QLabel("Rp 0")
            setattr(self, val_attr, label_val)
            row.addStretch(); row.addWidget(label_val)
            summary_layout.addLayout(row)

        add_sum_row("Subtotal:", "lbl_subtotal")
        
        disc_row = QHBoxLayout()
        disc_row.addWidget(QLabel("Potongan/Diskon:"))
        self.lbl_discount = QLabel("-Rp 0"); self.lbl_discount.setStyleSheet("color: #68d391;")
        disc_row.addStretch(); disc_row.addWidget(self.lbl_discount)
        summary_layout.addLayout(disc_row)
        
        summary_layout.addSpacing(20)
        
        total_row = QHBoxLayout()
        self.lbl_total_days = QLabel("Total (3 Hari):")
        self.lbl_grand_total = QLabel("Rp 0")
        self.lbl_grand_total.setStyleSheet("font-size: 20px; font-weight: 800;")
        total_row.addWidget(self.lbl_total_days)
        total_row.addStretch(); total_row.addWidget(self.lbl_grand_total)
        summary_layout.addLayout(total_row)

        btn_row = QVBoxLayout()
        btn_row.setSpacing(10)
        self.btn_submit = QPushButton("KONFIRMASI SEWA")
        self.btn_submit.setObjectName("confirm_btn")
        self.btn_submit.setFixedHeight(50)
        
        self.btn_save_draft = QPushButton("SIMPAN DRAFT")
        self.btn_save_draft.setFixedHeight(45)
        self.btn_save_draft.setObjectName("secondary_btn_light")
        
        btn_row.addWidget(self.btn_submit)
        btn_row.addWidget(self.btn_save_draft)
        summary_layout.addLayout(btn_row)

        right_side.addWidget(self.summary_card)
        right_side.addStretch()

        main_creation_content.addLayout(right_side, 1)
        self.scroll_layout.addLayout(main_creation_content)
        self.scroll_layout.addStretch()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget#scroll_content { background-color: white; }
            QFrame#white_card { background-color: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px; }
            QLabel { font-size: 11px; font-weight: 800; color: #4a5568; letter-spacing: 0.5px; }
            QLineEdit, QDateEdit, QSpinBox { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 15px; color: #2d3748; font-size: 13px; font-weight: 500; }
            QTableWidget { background-color: white; border: 1px solid #e2e8f0; border-radius: 12px; alternate-background-color: #f8fafc; selection-background-color: #f0fdf4; selection-color: #22543d; color: #2d3748; outline: none; }
            QHeaderView::section { background-color: white; padding: 8px 4px; border: none; border-bottom: 2px solid #edf2f7; color: #4a5568; font-weight: 700; font-size: 10px; text-transform: uppercase; }
            QPushButton#confirm_btn { background-color: transparent; color: white; border: 1px solid #718096; border-radius: 10px; font-weight: 900; font-size: 13px; letter-spacing: 1px; }
            QPushButton#secondary_btn { background-color: white; border: 1px solid #e2e8f0; border-radius: 8px; color: #4a5568; font-weight: 700; }
            QPushButton#detail_btn_table {
                background-color: white;
                border: 1px solid #cbd5e0;
                border-radius: 6px;
                color: #2d3748;
                font-size: 10px;
                font-weight: 700;
            }
            QPushButton#detail_btn_table:hover {
                background-color: #edf2f7;
                border-color: #a0aec0;
            }
            QPushButton#secondary_btn_light { 
                background-color: transparent; 
                border: 1px solid rgba(255, 255, 255, 0.4); 
                color: white; 
                border-radius: 10px; 
                font-weight: 700; 
            }
            QPushButton#secondary_btn_light:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-color: white;
            }
            
            QFrame#summary_card { background-color: #1e4d3a; border-radius: 16px; }
            QFrame#summary_card QLabel { color: #f0fff4; } /* Lighter green/white for readability */
            
            QLabel#total_big { font-size: 36px; font-weight: 900; color: #ffffff; margin: 15px 0; }
            
            /* Enhanced Action Button in Table */
            QPushButton#add_cart_btn {
                background-color: #234e3f;
                color: white;
                border-radius: 6px;
                font-weight: 800;
                font-size: 11px;
                padding: 0 10px;
            }
            QPushButton#add_cart_btn:hover {
                background-color: #2f6a55;
            }
            
            /* Main Confirmation Button */
            QPushButton#confirm_btn { 
                background-color: #ecc94b; /* Solid Yellow for high contrast */
                color: #1a3a2f; 
                border: none; 
                border-radius: 10px; 
                font-weight: 900; 
                font-size: 13px; 
                letter-spacing: 1px; 
            }
            QPushButton#confirm_btn:hover {
                background-color: #f6e05e;
            }

            QSpinBox#table_spin {
                min-width: 60px;
                max-width: 60px;
                height: 32px;
                padding: 0 5px;
            }
        """)

    def display_transactions(self, transactions):
        self.trans_table.setRowCount(len(transactions))
        for row, t in enumerate(transactions):
            date_item = QTableWidgetItem(t['tanggal_mulai'])
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.trans_table.setItem(row, 0, date_item)
            
            id_item = QTableWidgetItem(f"TR-{t['id'][:8].upper()}")
            id_item.setData(Qt.ItemDataRole.UserRole, t['id'])
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.trans_table.setItem(row, 1, id_item)
            
            customer_item = QTableWidgetItem(t['nama_pelanggan'])
            customer_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.trans_table.setItem(row, 2, customer_item)
            
            status_container = QWidget()
            status_layout = QHBoxLayout(status_container)
            status_layout.setContentsMargins(5, 5, 5, 5)
            display_status = self.status_map.get(t['status'], t['status'])
            status_btn = QPushButton(display_status)
            status_btn.setObjectName("status_badge_btn")
            status_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            colors = {
                'BOOKED': "background-color: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe;",
                'ACTIVE': "background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0;",
                'RETURNED': "background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a;",
                'CANCELLED': "background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca;"
            }
            status_btn.setStyleSheet(f"padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 700; {colors.get(t['status'], '')}")
            status_btn.clicked.connect(lambda _, tid=t['id'], s=display_status: self.show_status_menu(tid, s))
            status_layout.addWidget(status_btn)
            self.trans_table.setCellWidget(row, 3, status_container)
            
            view_btn = QPushButton("LIHAT DETAIL")
            view_btn.setObjectName("detail_btn_table") # Specific ID for table variant
            view_btn.setFixedSize(110, 32)
            view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            view_btn.clicked.connect(lambda _, tid=t['id']: self.request_show_details(tid))
            
            # Container for centering
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.addWidget(view_btn)
            self.trans_table.setCellWidget(row, 4, btn_container)
            
            total_item = QTableWidgetItem(f"Rp {t['total_biaya']:,}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.trans_table.setItem(row, 5, total_item)
            self.trans_table.setRowHeight(row, 50)

    def show_status_menu(self, trans_id, current_status):
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        for s in self.status_map.values():
            if s != current_status:
                action = menu.addAction(f"Tandai sebagai {s}")
                eng_status = self.reverse_status_map.get(s, s)
                action.triggered.connect(lambda _, st=eng_status: self.request_change_status(trans_id, st))
        menu.exec(self.cursor().pos())

    def update_cart_table(self):
        self.cart_table.setRowCount(len(self.cart))
        total = 0
        for row, item in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item['nama']))
            qty_item = QTableWidgetItem(str(item['jumlah']))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_table.setItem(row, 1, qty_item)
            price_item = QTableWidgetItem(f"Rp {item['harga']:,}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.cart_table.setItem(row, 2, price_item)
            btn = QPushButton("✕")
            btn.setFixedSize(24, 24)
            btn.setStyleSheet("background-color: #fee2e2; color: #991b1b; border: none; border-radius: 4px;")
            btn.clicked.connect(lambda _, r=row: self.request_remove_from_cart(r))
            self.cart_table.setCellWidget(row, 3, btn)
            total += item['harga']
        
        days = self.inp_start_date.date().daysTo(self.inp_end_date.date())
        if days < 1: days = 1
        self.lbl_total_days.setText(f"Total ({days} Hari):")
        self.lbl_subtotal.setText(f"Rp {total:,}")
        self.lbl_total_big.setText(f"Rp {total:,}")
        self.lbl_grand_total.setText(f"Rp {total:,}")

    def add_to_cart_logic(self, item, jumlah, harga):
        existing = next((x for x in self.cart if x['id_barang'] == item['id']), None)
        if existing:
            existing['jumlah'] += jumlah
            existing['harga'] += harga * jumlah
        else:
            self.cart.append({"id_barang": item['id'], "nama": item['nama'], "jumlah": jumlah, "harga": harga * jumlah})
        self.update_cart_table()

    def remove_from_cart_logic(self, row):
        if 0 <= row < len(self.cart):
            self.cart.pop(row)
            self.update_cart_table()

    def clear_form(self):
        self.cart = []
        self.update_cart_table()
        self.inp_name.clear()
        self.inp_contact.clear()

    def get_cart_data(self):
        return self.cart

    def display_available_items(self, items):
        self.avail_table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.avail_table.setItem(row, 0, QTableWidgetItem(item['nama']))
            stok_item = QTableWidgetItem(str(item.get('stok_tersedia', 0)))
            stok_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.avail_table.setItem(row, 1, stok_item)
            
            action_widget = QWidget()
            h_layout = QHBoxLayout(action_widget)
            h_layout.setContentsMargins(5, 5, 5, 5)
            h_layout.setSpacing(8)
            
            spin = QSpinBox()
            spin.setObjectName("table_spin")
            spin.setRange(1, item.get('stok_tersedia', 0) if item.get('stok_tersedia', 0) > 0 else 1)
            spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            btn = QPushButton("TAMBAH")
            btn.setObjectName("add_cart_btn")
            btn.setFixedHeight(32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, i=item, s=spin: self.request_add_to_cart(i, s.value()))
            
            h_layout.addStretch()
            h_layout.addWidget(spin)
            h_layout.addWidget(btn)
            h_layout.addStretch()
            
            self.avail_table.setCellWidget(row, 2, action_widget)
            self.avail_table.setRowHeight(row, 55)

    def show_transaction_details_dialog(self, items):
        dialog = QDialog(self)
        dialog.setWindowTitle("Detail Transaksi")
        dialog.setMinimumWidth(500)
        layout = QVBoxLayout(dialog)
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nama Barang", "Jumlah", "Harga"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setRowCount(len(items))
        total = 0
        for row, item in enumerate(items):
            nama_brg = item.get('barang', {}).get('nama', 'Unknown')
            table.setItem(row, 0, QTableWidgetItem(nama_brg))
            table.setItem(row, 1, QTableWidgetItem(str(item['jumlah'])))
            table.setItem(row, 2, QTableWidgetItem(f"Rp {item['harga_disepakati']:,}"))
            total += item['harga_disepakati'] * item['jumlah']
        layout.addWidget(table)
        total_lbl = QLabel(f"Total Biaya: Rp {total:,}")
        total_lbl.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        total_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(total_lbl)
        btn_close = QPushButton("Tutup"); btn_close.clicked.connect(dialog.accept); layout.addWidget(btn_close)
        dialog.exec()
