# 📂 Library Surat – Aplikasi Manajemen Surat (UAS)

Library Surat adalah aplikasi desktop berbasis **Python (PyQt6)** yang digunakan untuk
mengelola data **surat masuk dan surat keluar** secara digital.  
Aplikasi ini dibuat sebagai **Ujian Akhir Semester (UAS)** mata kuliah **Pemrograman Visual**.

Aplikasi mendukung pencatatan data surat, pencarian, penyimpanan arsip PDF, serta dapat
dikemas menjadi file **executable (.exe)** sehingga dapat dijalankan tanpa Python.

---

# 🎯 Tujuan Aplikasi
- Mengelola data surat masuk dan surat keluar
- Mempermudah pencarian arsip surat
- Menyimpan dokumen surat dalam bentuk PDF
- Menerapkan konsep pemrograman visual dengan PyQt6
- Mengimplementasikan packaging aplikasi menggunakan PyInstaller

---

# ✨ Fitur Aplikasi
- ✅ Input data surat (Tanggal, Kode, Nama, Asal, Tujuan)
- ✅ Pilihan jenis surat (Masuk / Keluar) menggunakan ComboBox
- ✅ Upload dan arsip surat dalam bentuk file PDF
- ✅ Membuka kembali file PDF langsung dari aplikasi
- ✅ Pencarian surat berdasarkan kode, nama, asal, atau tujuan
- ✅ Menampilkan data surat dalam tabel
- ✅ Menghapus data surat
- ✅ Mode tampilan gelap (Dark Mode)
- ✅ Packaging aplikasi menjadi file `.exe`

---

# 🛠️ Teknologi yang Digunakan
- Python 3
- PyQt6
- Supabase (Database & REST API)
- Requests
- PyInstaller
- Visual Studio Code

---

# 📦 Struktur Folder Project
LibrarySurat/
│
├── build # folder build aplikasi 
├── UAS.py # File utama aplikasi
├── pdf_surat/ # Folder penyimpanan file PDF surat
├── icon.ico # Icon aplikasi
├── README.md # Dokumentasi project
└── dist # folder apikasi exe

cara menggunakan aplikasi buka folder dist dan double klik file berbentuk .exe 
untuk cara menggunakan fiturnya cukup isi data yang di perlukan untuk menyimpannya kedalam database dan klik button sesuai kebutuhan
dan untuk menyimpan pdf cukup klik button khusus pdf dan untuk melihat pdf ada button khususnya juga 
