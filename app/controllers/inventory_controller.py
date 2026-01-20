from PyQt6.QtWidgets import (
    QMessageBox, QDialog, QFormLayout, QLineEdit, 
    QSpinBox, QPushButton, QLabel, QVBoxLayout, QWidget, QTabWidget
)

class InventoryController:
    def __init__(self, model, view):
        """
        [MVC - Controller]
        Menginisialisasi Controller Inventaris.
        Menghubungkan (Binding) logika bisnis ke interaksi UI (Signals & Slots).
        """
        self.model = model
        self.view = view
        
        # Hubungkan sinyal dari view ke metode controller
        self.view.btn_refresh.clicked.connect(self.refresh_data)
        self.view.btn_add.clicked.connect(self.show_add_dialog)
        self.view.btn_set_price.clicked.connect(self.show_price_dialog)
        
        # Baru: Pencarian dan Filter
        self.view.search_input.textChanged.connect(self.filter_data)
        self.view.cat_filter.currentTextChanged.connect(self.filter_data)
        
        # Baru: Tombol aksi dinamis
        self.view.request_manage_item = self.manage_item
        self.view.request_delete_item = self.delete_item

    def refresh_data(self):
        """
        [MVC - Controller]
        Mengambil data terbaru dari Model dan memperbarui tampilan via View.
        """
        try:
            self.all_items = self.model.get_all_items()
            self.filter_data()
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Gagal memuat data: {str(e)}")

    def delete_item(self, id_barang, nama_barang):
        """
        [MVC - Controller]
        Menangani permintaan penghapusan barang.
        Meminta konfirmasi ke user (via View) sebelum memerintahkan Model untuk menghapus data.
        """
        reply = QMessageBox.question(
            self.view, "Hapus Barang",
            f"Apakah Anda yakin ingin menghapus '{nama_barang}'?\nSemua histori harga juga akan dihapus.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.model.delete_item(id_barang)
                self.refresh_data()
                QMessageBox.information(self.view, "Sukses", f"Barang '{nama_barang}' telah dihapus.")
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Gagal menghapus: {str(e)}")

    def filter_data(self):
        """
        [MVC - Controller]
        Logika pemfilteran data (Pencarian & Kategori).
        Mengolah data mentah dari Model berdasarkan input user di View,
        lalu mengirimkan hasil filter kembali ke View untuk ditampilkan.
        """
        teks_cari = self.view.search_input.text().lower()
        filter_kategori = self.view.cat_filter.currentText()
        
        item_difilter = []
        for item in getattr(self, 'all_items', []):
            cocok_cari = teks_cari in item['nama'].lower() or teks_cari in item['kategori'].lower()
            cocok_kat = filter_kategori == "Semua Kategori" or item['kategori'] == filter_kategori
            
            if cocok_cari and cocok_kat:
                item_difilter.append(item)
                
        self.view.display_items(item_difilter)

    def manage_item(self, id_barang, nama_barang):
        """
        [MVC - Controller]
        Menyiapkan data spesifik barang untuk diedit.
        """
        item_detail = next((i for i in getattr(self, 'all_items', []) if i['id'] == id_barang), None)
        if item_detail:
            self.open_manage_dialog(item_detail)

    def open_manage_dialog(self, item):
        """
        [MVC - Controller]
        Membuka dialog 'Kelola Barang' (View).
        Controller mengatur isi awal form berdasarkan data yang ada.
        """
        id_barang = item['id']
        dialog = QDialog(self.view)
        dialog.setWindowTitle(f"Kelola Barang: {item['nama']}")
        dialog.setMinimumWidth(450)
        main_layout = QVBoxLayout(dialog)
        
        tabs = QTabWidget()
        
        # Tab 1: Edit Detail
        detail_tab = QWidget()
        detail_layout = QFormLayout(detail_tab)
        
        name_input = QLineEdit(item['nama'])
        category_input = QLineEdit(item['kategori'])
        stock_input = QSpinBox()
        stock_input.setRange(0, 1000)
        stock_input.setValue(item['stok_total'])
        
        detail_layout.addRow("Nama Barang:", name_input)
        detail_layout.addRow("Kategori:", category_input)
        detail_layout.addRow("Total Stok:", stock_input)
        
        btn_update = QPushButton("Update Informasi")
        btn_update.setFixedHeight(40)
        btn_update.setStyleSheet("background-color: #2b6cb0; color: white; font-weight: bold; border-radius: 6px;")
        btn_update.clicked.connect(lambda: self.update_item_info(dialog, id_barang, name_input.text(), category_input.text(), stock_input.value()))
        detail_layout.addRow(btn_update)
        
        tabs.addTab(detail_tab, "Informasi Dasar")
        
        # Tab 2: Harga
        price_tab = QWidget()
        price_layout = QFormLayout(price_tab)
        
        duration_input = QSpinBox()
        duration_input.setRange(1, 30)
        duration_input.setSuffix(" Hari")
        
        price_input = QSpinBox()
        price_input.setRange(0, 10000000)
        price_input.setSingleStep(5000)
        price_input.setPrefix("Rp ")
        
        price_layout.addRow("Durasi:", duration_input)
        price_layout.addRow("Harga:", price_input)
        
        btn_save_p = QPushButton("Simpan/Update Harga")
        btn_save_p.setFixedHeight(40)
        btn_save_p.setStyleSheet("background-color: #22543d; color: white; font-weight: bold; border-radius: 6px;")
        btn_save_p.clicked.connect(lambda: self.save_price(dialog, id_barang, duration_input.value(), price_input.value()))
        price_layout.addRow(btn_save_p)
        
        # Harga Saat Ini
        harga_ada = self.model.get_prices_for_item(id_barang)
        if harga_ada:
            info_label = QLabel("\nHarga Paket Saat Ini:")
            info_label.setStyleSheet("font-weight: bold; color: #2d3748;")
            price_layout.addRow(info_label)
            for p in harga_ada:
                lbl_duraci = QLabel(f"{p['durasi_hari']} Hari:")
                lbl_duraci.setStyleSheet("color: #2d3748; font-weight: bold;")
                lbl_harga = QLabel(f"Rp {p['harga']:,}")
                lbl_harga.setStyleSheet("color: #2d3748; font-weight: normal;")
                price_layout.addRow(lbl_duraci, lbl_harga)
                
        tabs.addTab(price_tab, "Paket Harga")
        
        main_layout.addWidget(tabs)
        dialog.exec()

    def update_item_info(self, dialog, id_barang, nama, kategori, stok):
        """
        [MVC - Controller]
        Memvalidasi input dari form edit dan meminta Model untuk menyimpan perubahan.
        """
        if not nama:
            QMessageBox.warning(dialog, "Validasi", "Nama barang harus diisi")
            return
        try:
            self.model.update_item(id_barang, {"nama": nama, "kategori": kategori, "stok_total": stok})
            self.refresh_data()
            QMessageBox.information(dialog, "Sukses", "Data barang berhasil diperbarui")
        except Exception as e:
            QMessageBox.critical(dialog, "Error", f"Gagal memperbarui: {str(e)}")

    def show_add_dialog(self):
        """
        [MVC - Controller]
        Membuka dialog untuk menambah barang baru.
        """
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Tambah Barang Baru")
        layout = QFormLayout(dialog)
        
        name_input = QLineEdit()
        category_input = QLineEdit()
        stock_input = QSpinBox()
        stock_input.setRange(0, 1000)
        
        layout.addRow("Nama Barang:", name_input)
        layout.addRow("Kategori:", category_input)
        layout.addRow("Total Stok:", stock_input)
        
        btn_save = QPushButton("Simpan")
        btn_save.clicked.connect(lambda: self.save_item(dialog, name_input.text(), category_input.text(), stock_input.value()))
        layout.addRow(btn_save)
        
        dialog.exec()

    def save_item(self, dialog, nama, kategori, stok):
        """
        [MVC - Controller]
        Menerima input barang baru, validasi, dan simpan via Model.
        """
        if not nama:
            QMessageBox.warning(dialog, "Validasi", "Nama barang harus diisi")
            return
            
        try:
            self.model.add_item(nama, kategori, stok)
            dialog.accept()
            self.refresh_data()
            QMessageBox.information(self.view, "Sukses", "Barang berhasil ditambahkan")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Gagal menyimpan: {str(e)}")

    def show_price_dialog(self):
        """
        [MVC - Controller]
        Membuka dialog pengaturan harga paket berdasarkan item yang dipilih di tabel.
        """
        data_item = self.view.get_selected_item()
        if not data_item:
            QMessageBox.warning(self.view, "Peringatan", "Pilih barang terlebih dahulu di tabel.")
            return
        
        id_barang, nama_barang = data_item
        item_detail = next((i for i in getattr(self, 'all_items', []) if i['id'] == id_barang), None)
        if item_detail:
            self.open_manage_dialog(item_detail)

    def save_price(self, dialog, id_barang, durasi, harga):
        """
        [MVC - Controller]
        Memerintahkan Model untuk menyimpan konfigurasi harga paket.
        """
        try:
            self.model.add_price_package(id_barang, durasi, harga)
            dialog.accept()
            QMessageBox.information(self.view, "Sukses", "Harga berhasil disimpan")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Gagal menyimpan harga: {str(e)}")
