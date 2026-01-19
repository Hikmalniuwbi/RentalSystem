# DOKUMENTASI TEKNIS: WILDERNESS ADMIN RENTAL SYSTEM

## 1. Arsitektur Folder
Aplikasi ini menggunakan pola desain **Model-View-Controller (MVC)** untuk memisahkan logika data, antarmuka, dan kontroler.

- `main.py`: Entry point aplikasi.
- `src/database.py`: Singleton untuk koneksi SQLite dan inisialisasi tabel.
- `src/models/`: Berisi logika query database (SQL).
- `src/views/`: Berisi desain antarmuka (PyQt6) yang dibangun secara programatik.
- `src/controllers/`: Menghubungkan Model dan View.

## 2. Struktur Database (SQLite)
Database lokal disimpan dalam file `rental_app.db` dengan skema bahasa Indonesia:

### Tabel `barang`
- `id` (TEXT, PK): UUID unik barang.
- `nama` (TEXT): Nama peralatan.
- `kategori` (TEXT): Kategori barang.
- `stok_total` (INTEGER): Total jumlah stok yang dimiliki.

### Tabel `harga_barang`
- `id_barang` (FK): Referensi ke tabel barang.
- `durasi_hari` (INTEGER): Durasi paket (misal: 1, 3, 7 hari).
- `harga` (INTEGER): Harga paket untuk durasi tersebut.

### Tabel `transaksi`
- `id` (TEXT, PK): ID unik transaksi (UUID).
- `nama_pelanggan` (TEXT): Nama penyewa.
- `kontak_pelanggan` (TEXT): Nomor telepon/WhatsApp.
- `tanggal_mulai` (TEXT): Tanggal mulai sewa (ISO format).
- `tanggal_selesai` (TEXT): Tanggal berakhir sewa (ISO format).
- `status` (TEXT): BOOKED, ACTIVE, RETURNED, CANCELLED.
- `total_biaya` (INTEGER): Total biaya yang harus dibayar.

## 3. Fitur Keamanan & Validasi
- **UUID**: Digunakan sebagai Primary Key untuk menjamin integritas data dan mencegah tebakan nomor transaksi secara urut.
- **Validasi Stok Real-Time**: Sistem menghitung stok tersedia dengan rumus: `Stok Total - Stok yang sedang dipinjam pada rentang tanggal tertentu`.
- **Foreign Key**: Menggunakan `PRAGMA foreign_keys = ON` untuk menjaga relasi antar tabel (misal: menghapus barang akan menghapus histori harganya).
