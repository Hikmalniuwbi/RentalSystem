# Manual Pengguna Kelana Outdoor Rental System

Selamat datang di Panduan Pengguna untuk **Kelana Outdoor Rental System**. Aplikasi ini dirancang untuk memudahkan pengelolaan penyewaan peralatan outdoor, mulai dari pendataan barang, pemantauan stok, hingga pencatatan transaksi sewa.

---

## DAFTAR ISI

1. [Memulai Aplikasi](#1-memulai-aplikasi)
2. [Navigasi Utama](#2-navigasi-utama)
3. [Dashboard](#3-dashboard)
4. [Manajemen Inventaris](#4-manajemen-inventaris)
5. [Manajemen Transaksi](#5-manajemen-transaksi)

---

## 1. MEMULAI APLIKASI

### Menjalankan Aplikasi

Pastikan Python dan dependensi yang diperlukan sudah terinstal.

1. Buka terminal atau command prompt.
2. Arahkan ke direktori proyek.
3. Jalankan perintah:
   ```bash
   python main.py
   ```
4. Jendela utama aplikasi akan muncul.

---

## 2. NAVIGASI UTAMA

Di sebelah kiri aplikasi terdapat **Sidebar Menu** yang berisi navigasi utama:

- **Dashboard**: Melihat ringkasan statistik dan aktivitas terbaru.
- **Inventaris**: Mengelola data barang (tambah, edit, hapus) dan stok.
- **Transaksi**: Melihat riwayat transaksi dan membuat transaksi penyewaan baru.

Di bagian atas terdapat **Header** yang berisi kolom pencarian cepat (_Quick Search_) dan informasi profil pengguna yang sedang login (Administrator).

---

## 3. DASHBOARD

Halaman Dashboard memberikan gambaran umum tentang operasional rental saat ini.

### Fitur Utama:

- **Kartu Statistik**: Menampilkan jumlah transaksi berdasarkan status:
  - **Booking**: Menunggu pengambilan barang.
  - **Sedang Di Pakai**: Barang sedang disewa pelanggan.
  - **Dikembalikan**: Transaksi selesai.
  - **Perawatan**: Barang sedang dalam maintenance.
- **Stok Real Time**: Ringkasan jumlah total stok, stok tersedia, dan stok yang sedang disewa.
- **Status Transaksi Terbaru**: Tabel mini yang menampilkan daftar transaksi terakhir untuk pemantauan cepat.
- **Tombol Pintas**: Akses cepat untuk membuat **Transaksi Baru** atau **Lihat Inventory**.

---

## 4. MANAJEMEN INVENTARIS

Menu ini digunakan untuk mengelola seluruh data peralatan outdoor.

### Tampilan Daftar Barang

Tabel inventaris menampilkan informasi:

- **ID & SKU**: Kode identifikasi barang.
- **Nama Item**: Nama peralatan.
- **Kategori**: Jenis peralatan (misal: Tenda, Tas, dll).
- **Status Stok**: Indikator warna (Hijau: Aman, Kuning: Hampir Habis, Merah: Habis).
- **Progress Bar**: Visualisasi persentase ketersediaan stok.

### Fitur & Aksi:

1. **Pencarian & Filter**:
   - Gunakan kolom pencarian untuk mencari barang berdasarkan nama.
   - Gunakan _dropdown_ kategori untuk menyaring jenis barang tertentu.
2. **Tambah Barang**:
   - Klik tombol **+ Tambah Barang**.
   - Isi formulir (Nama, Kategori, Stok Awal, Harga Sewa).
   - Klik Simpan.
3. **Kelola Item**:
   - Klik tombol **Kelola** pada baris barang yang diinginkan (atau klik kanan > Kelola Item).
   - Anda dapat mengedit detail barang atau menambah stok.
4. **Hapus Item**:
   - Klik tombol **Hapus** (atau klik kanan > Hapus Item) untuk menghapus barang dari database.
   - _Hati-hati: Aksi ini permanen._

---

## 5. MANAJEMEN TRANSAKSI

Halaman ini dibagi menjadi dua bagian utama: **Riwayat Transaksi** dan **Buat Transaksi Baru**.

### A. Riwayat Transaksi (History)

Daftar seluruh transaksi yang pernah dilakukan.

- **Pencarian**: Filter riwayat berdasarkan ID Transaksi atau Nama Pelanggan.
- **Status Badge**: Warna berbeda untuk setiap status (Booking, Aktif, Dikembalikan, Dibatalkan).
- **Lihat Detail**: Klik tombol "LIHAT DETAIL" untuk melihat rincian barang yang disewa pada transaksi tersebut.
- **Ubah Status**:
  - Klik pada badge status (misal: "BOOKING") untuk memunculkan menu.
  - Pilih status baru (misal: ubah dari "BOOKING" ke "AKTIF" saat barang diambil).

### B. Buat Transaksi Baru

Formulir untuk mencatat penyewaan baru.

**Langkah-langkah:**

1. **Data Pelanggan**:
   - Isi **Nama Pelanggan** dan **No. Kontak**.
2. **Tanggal Sewa**:
   - Tentukan **Tanggal Sewa** (pengambilan) dan **Tanggal Kembali**.
   - Sistem akan otomatis menghitung durasi hari.
3. **Pilih Barang**:
   - Di bagian "Barang Tersedia", cari barang yang diinginkan.
   - Masukkan jumlah pada kotak angka.
   - Klik tombol **TAMBAH**. Barang akan masuk ke tabel "Keranjang (Cart)".
4. **Keranjang (Cart)**:
   - Daftar barang yang akan disewa muncul di sini.
   - Klik tanda silang (X) merah untuk membatalkan item dari keranjang.
5. **Konfirmasi Pembayaran**:
   - Periksa **Subtotal** dan **Total Biaya** (dikalikan durasi hari).
   - Klik **KONFIRMASI SEWA** untuk menyimpan transaksi.
   - Transaksi akan masuk ke riwayat dengan status awal "BOOKED" atau "ACTIVE".

---

**Catatan Tambahan:**

- Pastikan untuk selalu memeriksa ketersediaan stok sebelum membuat transaksi.
- Gunakan fitur "Refresh" jika data tampaknya belum diperbarui.

_Dibuat untuk kebutuhan operasional Kelana Outdoor._
