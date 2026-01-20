from app.database import Database
from datetime import date
import uuid

class TransaksiModel:
    def __init__(self):
        """
        [MVC - Model]
        Inisialisasi model transaksi.
        Membuka koneksi database.
        """
        self.conn = Database.get_connection()

    def cek_ketersediaan(self, id_barang: str, tanggal_mulai: date, tanggal_selesai: date):
        """
        [MVC - Model]
        Logika Bisnis Compleks:
        Mengecek apakah barang tersedia pada rentang tanggal yang diminta.
        Menghitung stok total dikurangi barang yang sedang di-booking/aktif pada tanggal tersebut.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT stok_total FROM barang WHERE id = ?", (id_barang,))
        res = cursor.fetchone()
        if not res: return 0
        stok_total = res['stok_total']

        s_date_str = tanggal_mulai.isoformat()
        e_date_str = tanggal_selesai.isoformat()
        
        cursor.execute("""
            SELECT SUM(it.jumlah) as digunakan
            FROM item_transaksi it
            JOIN transaksi t ON it.id_transaksi = t.id
            WHERE it.id_barang = ?
              AND t.status NOT IN ('RETURNED', 'CANCELLED')
              AND t.tanggal_mulai <= ? AND t.tanggal_selesai >= ?
        """, (id_barang, e_date_str, s_date_str))
        
        res = cursor.fetchone()
        digunakan = res['digunakan'] if res and res['digunakan'] else 0
        return max(0, stok_total - digunakan)

    def create_transaksi(self, data_transaksi, data_item):
        """
        [MVC - Model]
        Menyimpan transaksi baru beserta item-itemnya secara atomik.
        Menerima data dari Controller yang sudah divalidasi.
        """
        id_transaksi = str(uuid.uuid4())
        data_transaksi['id'] = id_transaksi
        
        cursor = self.conn.cursor()
        
        # SISIPKAN TRANSAKSI
        keys = data_transaksi.keys()
        values = list(data_transaksi.values())
        placeholders = ", ".join(["?" for _ in keys])
        columns = ", ".join(keys)
        query = f"INSERT INTO transaksi ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(values))
        
        # SISIPKAN ITEM
        for item in data_item:
            cursor.execute("""
                INSERT INTO item_transaksi (id_transaksi, id_barang, jumlah, harga_disepakati)
                VALUES (?, ?, ?, ?)
            """, (id_transaksi, item['id_barang'], item['jumlah'], item['harga_disepakati']))
            
        self.conn.commit()
        return id_transaksi
    
    def get_all_transactions(self):
        """
        [MVC - Model]
        Mengambil riwayat semua transaksi untuk keperluan pelaporan/dashboard.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transaksi ORDER BY tanggal_mulai DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_active_transactions(self):
        """
        [MVC - Model]
        Mengambil hanya transaksi yang sedang berjalan (BOOKED atau ACTIVE).
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM transaksi 
            WHERE status IN ('BOOKED', 'ACTIVE') 
            ORDER BY tanggal_mulai DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
            
    def update_status(self, id_transaksi, status_baru):
        """
        [MVC - Model]
        Memperbarui status transaksi (misal: dari BOOKED -> ACTIVE, atau ACTIVE -> RETURNED).
        """
        cursor = self.conn.cursor()
        cursor.execute("UPDATE transaksi SET status = ? WHERE id = ?", (status_baru, id_transaksi))
        self.conn.commit()
        return True

    def get_transaction_items(self, id_transaksi):
        """
        [MVC - Model]
        Mengambil detail item apa saja yang disewa dalam satu ID transaksi.
        Melakukan JOIN dengan tabel barang untuk mendapatkan nama barang.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT it.jumlah, it.harga_disepakati, b.nama 
            FROM item_transaksi it
            JOIN barang b ON it.id_barang = b.id
            WHERE it.id_transaksi = ?
        """, (id_transaksi,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'jumlah': row['jumlah'],
                'harga_disepakati': row['harga_disepakati'],
                'barang': {'nama': row['nama']}
            })
        return results
