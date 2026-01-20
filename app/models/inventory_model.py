from app.database import Database
from datetime import date
import uuid

class InventoryModel:
    def __init__(self):
        """
        [MVC - Model]
        Inisialisasi model inventaris.
        Membuka koneksi ke database untuk melakukan operasi CRUD.
        """
        self.conn = Database.get_connection()

    def get_all_items(self):
        """
        [MVC - Model]
        Mengambil semua data barang dari database.
        Melakukan logika bisnis untuk menghitung 'stok_tersedia' secara real-time
        berdasarkan transaksi yang sedang aktif pada hari ini.
        Returns:
            list: Daftar dictionary barang dengan stok terkini.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM barang ORDER BY nama")
        items = [dict(row) for row in cursor.fetchall()]
        
        today = date.today().isoformat()
        
        for item in items:
            cursor.execute("""
                SELECT SUM(it.jumlah) as digunakan
                FROM item_transaksi it
                JOIN transaksi t ON it.id_transaksi = t.id
                WHERE it.id_barang = ? 
                  AND t.status NOT IN ('RETURNED', 'CANCELLED')
                  AND t.tanggal_mulai <= ? AND t.tanggal_selesai >= ?
            """, (item['id'], today, today))
            
            res = cursor.fetchone()
            digunakan = res['digunakan'] if res and res['digunakan'] else 0
            item['stok_tersedia'] = max(0, item['stok_total'] - digunakan)
            
        return items

    def add_item(self, nama: str, kategori: str, stok_total: int):
        """
        [MVC - Model]
        Menambahkan barang baru ke database (Create).
        Model bertanggung jawab memastikan data tersimpan ke tabel 'barang'.
        """
        id_baru = str(uuid.uuid4())
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO barang (id, nama, kategori, stok_total) VALUES (?, ?, ?, ?)",
            (id_baru, nama, kategori, stok_total)
        )
        self.conn.commit()
        return {"id": id_baru, "nama": nama, "kategori": kategori, "stok_total": stok_total}

    def update_item(self, id_barang: str, updates: dict):
        """
        [MVC - Model]
        Memperbarui atribut barang (nama, kategori, stok) di database (Update).
        Menerima dictionary 'updates' yang berisi field yang akan diubah.
        """
        # Petakan kunci internal ke nama kolom dalam Bahasa Indonesia jika perlu
        # Asumsikan dict pembaruan sudah menggunakan kunci Bahasa Indonesia dari view/controller
        # Asumsikan dict pembaruan menggunakan nama kolom DB secara langsung untuk kesederhanaan.
        keys = updates.keys()
        values = list(updates.values())
        values.append(id_barang)
        
        set_clause = ", ".join([f"{k} = ?" for k in keys])
        query = f"UPDATE barang SET {set_clause} WHERE id = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, tuple(values))
        self.conn.commit()
        return updates

    def delete_item(self, id_barang: str):
        """
        [MVC - Model]
        Menghapus barang dari database berdasarkan ID (Delete).
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM barang WHERE id = ?", (id_barang,))
        self.conn.commit()
        return True

    def add_price_package(self, id_barang: str, durasi_hari: int, harga: int):
        """
        [MVC - Model]
        Menambahkan atau memperbarui skema harga sewa untuk durasi tertentu.
        Menggunakan logika 'ON CONFLICT' untuk handle insert/update sekaligus.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO harga_barang (id_barang, durasi_hari, harga) 
            VALUES (?, ?, ?)
            ON CONFLICT(id_barang, durasi_hari) DO UPDATE SET harga = excluded.harga
        """, (id_barang, durasi_hari, harga))
        self.conn.commit()
        return True

    def get_prices_for_item(self, id_barang: str):
        """
        [MVC - Model]
        Mengambil daftar paket harga yang tersedia untuk suatu barang.
        Data ini akan dikirim ke View melalui Controller untuk ditampilkan.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM harga_barang WHERE id_barang = ? ORDER BY durasi_hari", (id_barang,))
        return [dict(row) for row in cursor.fetchall()]

    def calculate_price(self, id_barang: str, tanggal_mulai, tanggal_selesai):
        """
        [MVC - Model]
        Logika bisnis untuk menghitung estimasi biaya sewa berdasarkan durasi.
        Model melakukan kalkulasi murni tanpa mempedulikan UI.
        """
        durasi = (tanggal_selesai - tanggal_mulai).days
        if durasi < 1: durasi = 1
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT harga FROM harga_barang WHERE id_barang = ? AND durasi_hari = ?", (id_barang, durasi))
        res = cursor.fetchone()
        return res['harga'] if res else None
