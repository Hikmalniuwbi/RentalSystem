import sqlite3

class Database:
    _instance = None
    DB_NAME = "rental_app.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(cls.DB_NAME)
            cls._instance.conn.execute("PRAGMA foreign_keys = ON")
            cls._instance.conn.row_factory = sqlite3.Row
        return cls._instance

    @classmethod
    def get_connection(cls):
        return cls().conn

    def init_db(self):
        cursor = self.conn.cursor()
        
        # Tabel barang
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS barang (
                id TEXT PRIMARY KEY,
                nama TEXT NOT NULL,
                kategori TEXT,
                stok_total INTEGER DEFAULT 0
            )
        """)

        # Tabel harga_barang
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS harga_barang (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_barang TEXT,
                durasi_hari INTEGER,
                harga INTEGER,
                UNIQUE(id_barang, durasi_hari),
                FOREIGN KEY (id_barang) REFERENCES barang(id) ON DELETE CASCADE
            )
        """)

        # Tabel transaksi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id TEXT PRIMARY KEY,
                nama_pelanggan TEXT,
                kontak_pelanggan TEXT,
                tanggal_mulai TEXT,
                tanggal_selesai TEXT,
                status TEXT,
                total_biaya INTEGER
            )
        """)

        # Tabel item_transaksi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_transaksi TEXT,
                id_barang TEXT,
                jumlah INTEGER,
                harga_disepakati INTEGER,
                FOREIGN KEY (id_transaksi) REFERENCES transaksi(id) ON DELETE CASCADE,
                FOREIGN KEY (id_barang) REFERENCES barang(id)
            )
        """)

        self.conn.commit()
