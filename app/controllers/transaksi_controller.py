from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from datetime import date

class TransaksiController:
    def __init__(self, model, inventory_model, view):
        self.model = model
        self.inventory_model = inventory_model
        self.view = view
        
        # Hubungkan sinyal
        self.view.search_item.textChanged.connect(self.filter_items)
        self.view.search_trans.textChanged.connect(self.filter_transactions)
        self.view.btn_submit.clicked.connect(lambda: self.submit_booking("BOOKED"))
        self.view.btn_save_draft.clicked.connect(self.save_as_draft)
        self.view.btn_refresh_dashboard.clicked.connect(self.refresh_all)
        
        # Perubahan tanggal harus memperbarui harga keranjang
        self.view.inp_start_date.dateChanged.connect(self.refresh_cart_prices)
        self.view.inp_end_date.dateChanged.connect(self.refresh_cart_prices)
        
        # Masukkan logika kustom ke elemen dinamis view jika diperlukan
        self.view.request_add_to_cart = self.add_item_to_cart
        self.view.request_change_status = self.change_status
        self.view.request_show_details = self.show_details
        self.view.request_remove_from_cart = self.remove_from_cart

    def refresh_all(self):
        self.load_available_items()
        self.refresh_dashboard()

    def load_available_items(self):
        try:
            items = self.inventory_model.get_all_items()
            self.view.all_items = items
            self.view.display_available_items(items)
        except Exception as e:
            print(f"Gagal memuat barang: {e}")

    def filter_items(self, text):
        filtered = [item for item in getattr(self.view, 'all_items', []) if text.lower() in item['nama'].lower()]
        self.view.display_available_items(filtered)

    def filter_transactions(self, text):
        try:
            all_trans = self.model.get_all_transactions()
            filtered = [
                t for t in all_trans 
                if text.lower() in t['nama_pelanggan'].lower() or text.lower() in t['id'].lower()
            ]
            self.view.display_transactions(filtered)
        except Exception as e:
            print(f"Error filtering transactions: {e}")

    def save_as_draft(self):
        self.submit_booking(status="BOOKED") 

    def refresh_cart_prices(self):
        tanggal_mulai = self.view.inp_start_date.date().toPyDate()
        tanggal_selesai = self.view.inp_end_date.date().toPyDate()
        
        if tanggal_selesai <= tanggal_mulai:
            return 
            
        for item in self.view.cart:
            try:
                harga = self.inventory_model.calculate_price(item['id_barang'], tanggal_mulai, tanggal_selesai)
                if harga:
                    item['harga'] = harga * item['jumlah']
            except Exception:
                pass
        self.view.update_cart_table()

    def add_item_to_cart(self, item, jumlah):
        # Kita cek available_stock (dihitung di model sebagai stok_tersedia)
        if item.get('stok_tersedia', 0) < jumlah:
            QMessageBox.warning(self.view, "Stok Kurang", "Stok tidak mencukupi hari ini.")
            return

        tanggal_mulai = self.view.inp_start_date.date().toPyDate()
        tanggal_selesai = self.view.inp_end_date.date().toPyDate()
        
        if tanggal_selesai <= tanggal_mulai:
            QMessageBox.warning(self.view, "Tanggal Salah", "Tanggal kembali harus setelah tanggal sewa.")
            return

        try:
            harga = self.inventory_model.calculate_price(item['id'], tanggal_mulai, tanggal_selesai)
            if harga is None:
                QMessageBox.warning(self.view, "Harga Tidak Ada", f"Paket harga untuk durasi {(tanggal_selesai - tanggal_mulai).days} hari belum diatur.")
                return

            self.view.add_to_cart_logic(item, jumlah, harga)
        except Exception as e:
            QMessageBox.critical(self.view, "Error", str(e))

    def remove_from_cart(self, row):
        self.view.remove_from_cart_logic(row)

    def submit_booking(self, status="BOOKED"):
        keranjang = self.view.get_cart_data()
        if not keranjang:
            QMessageBox.warning(self.view, "Kosong", "Keranjang belanja kosong.")
            return
            
        nama = self.view.inp_name.text()
        kontak = self.view.inp_contact.text()
        tanggal_mulai = self.view.inp_start_date.date().toPyDate()
        tanggal_selesai = self.view.inp_end_date.date().toPyDate()
        
        if not nama or not kontak:
            QMessageBox.warning(self.view, "Data Kurang", "Nama dan Kontak wajib diisi.")
            return
            
        try:
            line_items_data = []
            total_biaya = 0

            for x in keranjang:
                tersedia = self.model.cek_ketersediaan(x['id_barang'], tanggal_mulai, tanggal_selesai)
                if tersedia < x['jumlah']:
                    raise ValueError(f"Stok tidak mencukupi untuk item {x['nama']}. Tersedia: {tersedia}")
                
                harga = self.inventory_model.calculate_price(x['id_barang'], tanggal_mulai, tanggal_selesai)
                if harga is None:
                    raise ValueError(f"Harga tidak ditemukan untuk {x['nama']}")
                
                total_biaya += harga * x['jumlah']
                line_items_data.append({
                    "id_barang": x['id_barang'],
                    "jumlah": x['jumlah'],
                    "harga_disepakati": harga
                })

            trans_data = {
                "nama_pelanggan": nama,
                "kontak_pelanggan": kontak,
                "tanggal_mulai": tanggal_mulai.isoformat(),
                "tanggal_selesai": tanggal_selesai.isoformat(),
                "status": status,
                "total_biaya": total_biaya
            }
            
            id_transaksi = self.model.create_transaksi(trans_data, line_items_data)
            
            QMessageBox.information(self.view, "Sukses", f"Booking berhasil dibuat! ID: {id_transaksi}")
            
            self.view.clear_form()
            self.refresh_dashboard()
            
        except ValueError as ve:
            QMessageBox.warning(self.view, "Gagal Validasi", str(ve))
        except Exception as e:
            QMessageBox.critical(self.view, "Error System", str(e))

    def refresh_dashboard(self):
        try:
            transaksi = self.model.get_all_transactions()
            self.view.display_transactions(transaksi)
        except Exception as e:
            print(f"Error loading dashboard: {e}")

    def show_details(self, id_transaksi):
        try:
            items = self.model.get_transaction_items(id_transaksi)
            if not items:
                QMessageBox.information(self.view, "Detail", "Tidak ada item dalam transaksi ini.")
                return
            
            self.view.show_transaction_details_dialog(items)
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Gagal memuat detail: {str(e)}")

    def change_status(self, id_transaksi, status_baru):
        try:
            self.model.update_status(id_transaksi, status_baru)
            self.refresh_dashboard()
            QMessageBox.information(self.view, "Update", f"Status berhasil diubah ke {status_baru}")
        except Exception as e:
            QMessageBox.critical(self.view, "Error", str(e))
