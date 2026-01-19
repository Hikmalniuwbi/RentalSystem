# LAPORAN PROYEK: SISTEM INFORMASI PERSEWAAN OUTDOOR

**Mata Kuliah:** Pemrograman Visual  
**Proyek:** Wilderness Admin Rental System  
**Penyusun:** [Nama Anda]

---

## I. Pendahuluan
### 1.1 Masalah
Manajemen persewaan peralatan outdoor sering mengalami kendala dalam pemantauan stok yang tersedia (available stock) pada tanggal tertentu, terutama saat terjadi tumpang tindih pesanan (overlap booking).

### 1.2 Solusi
Wilderness Admin hadir sebagai aplikasi desktop yang mampu memvalidasi ketersediaan stok secara otomatis berdasarkan rentang tanggal sewa, sehingga mencegah kesalahan manusia (*human error*) dalam pencatatan stok.

## II. Implementasi Sistem
### 2.1 Teknologi
Aplikasi dibangun menggunakan **Python** dengan library **PyQt6** untuk antarmuka yang modern dan profesional. Penyimpanan data menggunakan **SQLite** agar aplikasi bersifat *portable* dan tidak memerlukan server internet.

### 2.2 Pola MVC
Pemisahan kode menjadi Model, View, dan Controller memudahkan pengembangan berkelanjutan. Bagian **Model** bertanggung jawab menghitung stok aktif di database, sementara **View** menangani tampilan tabel yang bersih.

## III. Hasil dan Pembahasan
- **Manajemen Harga Fleksibel**: Pemilik bisnis dapat mengatur harga yang berbeda untuk durasi sewa yang berbeda (misal: sewa 3 hari lebih murah per harinya dibanding sewa 1 hari).
- **Dashboard Ringkas**: Grafik angka (Booking, Aktif, Selesai) memudahkan pemilik melihat performa harian secara cepat.
- **Validasi Cerdas**: Tombol penambah barang ke keranjang akan terkunci atau memberi peringatan jika stok pada tanggal tersebut sudah habis dipesan orang lain.

## IV. Kesimpulan
Sistem ini berhasil mendigitalisasi proses persewaan yang dulunya manual menjadi otomatis, mulai dari pengecekan stok, penghitungan total harga paket, hingga manajemen status barang (dikembalikan atau sedang dipakai).
