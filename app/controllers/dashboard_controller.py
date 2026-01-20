from PyQt6.QtWidgets import QMessageBox

class DashboardController:
    def __init__(self, inventory_model, rental_model, view, main_window):
        """
        [MVC - Controller]
        Controller Dashboard bertindak sebagai koordinator utama.
        Menggabungkan data dari berbagai Model (Inventory & Rental)
        untuk disajikan dalam satu View (DashboardView).
        """
        self.inventory_model = inventory_model
        self.rental_model = rental_model
        self.view = view
        self.main_window = main_window
        
        # Connect signals
        self.view.btn_new_trans.clicked.connect(lambda: self.main_window.menu_list.setCurrentRow(2))
        self.view.btn_view_inventory.clicked.connect(lambda: self.main_window.menu_list.setCurrentRow(1))
        
        self.refresh_data()

    def refresh_data(self):
        """
        [MVC - Controller]
        Mengumpulkan dan mengolah ringkasan data.
        1. Mengambil data transaksi dari RentalModel.
        2. Mengambil data stok dari InventoryModel.
        3. Menghitung statistik (Booked, Active, Returned, dll).
        4. Memperbarui DashboardView dengan angka-angka terbaru.
        """
        try:
            # 1. Get Transaction Counts
            transaksi = self.rental_model.get_all_transactions()
            booked = len([t for t in transaksi if t['status'] == 'BOOKED'])
            aktif = len([t for t in transaksi if t['status'] == 'ACTIVE'])
            kembali = len([t for t in transaksi if t['status'] == 'RETURNED'])
            batal = len([t for t in transaksi if t['status'] == 'CANCELLED'])
            
            perawatan = 0 
            
            # 2. Get Stock Summary
            barang = self.inventory_model.get_all_items()
            stok_total = sum(b['stok_total'] for b in barang)
            stok_tersedia = sum(b.get('stok_tersedia', 0) for b in barang)
            stok_keluar = stok_total - stok_tersedia
            
            ringkasan_stok = {
                'total': stok_total,
                'avail': stok_tersedia,
                'out': stok_keluar
            }
            
            self.view.update_stats(booked, aktif, kembali, perawatan, ringkasan_stok)
            
            # 3. Update mini table with latest 5 transactions
            terbaru = transaksi[:5]
            self.view.mini_table.setRowCount(len(terbaru))
            
            from PyQt6.QtWidgets import QTableWidgetItem
            from PyQt6.QtCore import Qt
            
            for baris, t in enumerate(terbaru):
                self.view.mini_table.setItem(baris, 0, QTableWidgetItem(f"#{t['id'][:6].upper()}"))
                nama_pelanggan_item = QTableWidgetItem(t['nama_pelanggan'])
                nama_pelanggan_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.mini_table.setItem(baris, 1, nama_pelanggan_item)
                
                status_item = QTableWidgetItem(t['status'])
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.mini_table.setItem(baris, 2, status_item)
                
                biaya_item = QTableWidgetItem(f"Rp {t['total_biaya']:,}")
                biaya_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.view.mini_table.setItem(baris, 3, biaya_item)
            
            self.view.mini_table.setRowHeight(baris, 40) if terbaru else None
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
