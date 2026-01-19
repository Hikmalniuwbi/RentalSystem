from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt

class StatCard(QFrame):
    def __init__(self, title, value, detail, icon, icon_color, parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card")
        self.setFixedHeight(120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        top_row = QHBoxLayout()
        title_label = QLabel(title.upper())
        title_label.setObjectName("stat_title")
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"color: {icon_color}; font-size: 18px;")
        top_row.addWidget(title_label)
        top_row.addStretch()
        top_row.addWidget(icon_label)
        layout.addLayout(top_row)
        
        self.val_label = QLabel(str(value))
        self.val_label.setObjectName("stat_value")
        layout.addWidget(self.val_label)
        
        self.detail_label = QLabel(detail)
        self.detail_label.setObjectName("stat_detail")
        layout.addWidget(self.detail_label)
        
        self.setStyleSheet(f"""
            QFrame#stat_card {{
                background-color: white;
                border: 1px solid #e2e8f0;
                border-bottom: 3px solid {icon_color}; /* Accent border */
                border-radius: 12px;
            }}
            QFrame#stat_card:hover {{
                border-color: {icon_color};
                background-color: #fcfcfc;
            }}
            QLabel#stat_title {{
                color: #4a5568;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            QLabel#stat_value {{
                color: #1a202c;
                font-size: 32px;
                font-weight: 900;
            }}
            QLabel#stat_detail {{
                color: #38a169;
                font-size: 11px;
                font-weight: 700;
            }}
        """)

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def update_stats(self, booked, in_use, returned, maintenance, stock_summary):
        self.card_booked.val_label.setText(str(booked))
        self.card_in_use.val_label.setText(str(in_use))
        self.card_returned.val_label.setText(str(returned))
        self.card_maint.val_label.setText(str(maintenance))
        
        # Update Stock Summary Circles
        # Assuming stock_summary = {'total': X, 'avail': Y, 'out': Z}
        # We need to find the labels and update them. 
        # Since we didn't store references, let's refactor the init_ui slightly to store them or just find them.
        # Actually, let's just refactor to store them.
        self.lbl_stock_total.setText(str(stock_summary.get('total', 0)))
        self.lbl_stock_avail.setText(str(stock_summary.get('avail', 0)))
        self.lbl_stock_out.setText(str(stock_summary.get('out', 0)))

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(30)

        # Header
        header_layout = QHBoxLayout()
        v_box = QVBoxLayout()
        title = QLabel("Dashboard Overview")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: #234e3f;")
        v_box.addWidget(title)
      
        header_layout.addLayout(v_box)
        header_layout.addStretch()
        
        self.btn_new_trans = QPushButton("+ Transaksi Baru")
        self.btn_new_trans.setStyleSheet("background-color: #234e3f; color: white; border-radius: 8px; padding: 12px 20px; font-weight: bold;")
        header_layout.addWidget(self.btn_new_trans)
        
        self.main_layout.addLayout(header_layout)

        # Stats Grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        
        self.card_booked = StatCard("Booking", "0", "Menunggu Pick Up", "", "#3182ce")
        self.card_in_use = StatCard("Sedang Di Pakai", "0", "Sedang Di Pakai", "", "#38a169")
        self.card_returned = StatCard("Dikembalikan", "0", "Dikembalikan", "", "#dd6b20")
        self.card_maint = StatCard("Perawatan", "0", "Perawatan", "", "#e53e3e")
        
        stats_layout.addWidget(self.card_booked, 0, 0)
        stats_layout.addWidget(self.card_in_use, 0, 1)
        stats_layout.addWidget(self.card_returned, 0, 2)
        stats_layout.addWidget(self.card_maint, 0, 3)
        
        self.main_layout.addLayout(stats_layout)

        # Middle Content (Splitter or Row)
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(25)
        
        # Real-time Stock Card
        stock_frame = QFrame()
        stock_frame.setObjectName("content_card")
        stock_layout = QVBoxLayout(stock_frame)
        stock_layout.setContentsMargins(25, 25, 25, 25)
        
        stock_header = QHBoxLayout()
        sh_label = QLabel("STOK REAL TIME")
        sh_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #2d3748;")
        live_badge = QLabel("LIVE")
        live_badge.setStyleSheet("background-color: #f0fff4; color: #38a169; border: 1px solid #c6f6d5; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 800;")
        stock_header.addWidget(sh_label); stock_header.addStretch(); stock_header.addWidget(live_badge)
        stock_layout.addLayout(stock_header)
        stock_layout.addSpacing(20)
        
        # Summary circles
        sum_layout = QHBoxLayout()
        sum_layout.setSpacing(40)
        
        v1 = QVBoxLayout(); l11 = QLabel("TOTAL STOK"); l11.setStyleSheet("color: #718096; font-size: 11px; font-weight: 800;")
        self.lbl_stock_total = QLabel("0"); self.lbl_stock_total.setStyleSheet("color: #2d3748; font-size: 28px; font-weight: 900;")
        v1.addWidget(l11, 0, Qt.AlignmentFlag.AlignCenter); v1.addWidget(self.lbl_stock_total, 0, Qt.AlignmentFlag.AlignCenter)
        sum_layout.addLayout(v1)
        
        v2 = QVBoxLayout(); l21 = QLabel("KETERSEDIAAN"); l21.setStyleSheet("color: #38a169; font-size: 11px; font-weight: 800;")
        self.lbl_stock_avail = QLabel("0"); self.lbl_stock_avail.setStyleSheet("color: #38a169; font-size: 28px; font-weight: 900;")
        v2.addWidget(l21, 0, Qt.AlignmentFlag.AlignCenter); v2.addWidget(self.lbl_stock_avail, 0, Qt.AlignmentFlag.AlignCenter)
        sum_layout.addLayout(v2)
        
        v3 = QVBoxLayout(); l31 = QLabel("DISEWA"); l31.setStyleSheet("color: #3182ce; font-size: 11px; font-weight: 800;")
        self.lbl_stock_out = QLabel("0"); self.lbl_stock_out.setStyleSheet("color: #3182ce; font-size: 28px; font-weight: 900;")
        v3.addWidget(l31, 0, Qt.AlignmentFlag.AlignCenter); v3.addWidget(self.lbl_stock_out, 0, Qt.AlignmentFlag.AlignCenter)
        sum_layout.addLayout(v3)

        stock_layout.addLayout(sum_layout)
        stock_layout.addStretch()
        self.btn_view_inventory = QPushButton("Lihat Inventory")
        stock_layout.addWidget(self.btn_view_inventory)
        
        mid_layout.addWidget(stock_frame, 1)

        # Transaction Status Card
        trans_frame = QFrame()
        trans_frame.setObjectName("content_card")
        trans_layout = QVBoxLayout(trans_frame)
        trans_layout.setContentsMargins(25, 25, 25, 25)
        
        trans_header = QHBoxLayout()
        th_label = QLabel("STATUS TRANSAKSI")
        th_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #2d3748;")
        trans_header.addWidget(th_label); trans_header.addStretch()
        trans_layout.addLayout(trans_header)
        
        # Mini table for recent activity
        self.mini_table = QTableWidget()
        self.mini_table.setColumnCount(4)
        self.mini_table.setHorizontalHeaderLabels(["ID", "KOSTUMER", "STATUS", "JUMLAH"])
        self.mini_table.verticalHeader().setVisible(False)
        self.mini_table.setShowGrid(False)
        self.mini_table.setAlternatingRowColors(True)
        self.mini_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.mini_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        header = self.mini_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setStyleSheet("QHeaderView::section { background-color: transparent; border: none; color: #4a5568; font-weight: 800; font-size: 11px; text-transform: uppercase; }")
        
        self.mini_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                alternate-background-color: #f8fafc;
            }
            QTableWidget::item {
                padding: 8px;
                color: #2d3748;
                font-size: 12px;
                border-bottom: 1px solid #edf2f7;
            }
        """)
        
        trans_layout.addWidget(self.mini_table)
        
        mid_layout.addWidget(trans_frame, 2)
        
        self.main_layout.addLayout(mid_layout)
        self.main_layout.addStretch()

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QFrame#content_card {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px;
                font-weight: 700;
                color: #4a5568;
            }
            QPushButton:hover {
                border-color: #38a169;
                color: #38a169;
            }
        """)
