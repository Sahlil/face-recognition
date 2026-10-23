# Aplikasi Pengenilan Wajah (Face Recognition App)

Aplikasi ini adalah sistem pengenalan wajah sederhana yang terdiri dari dua komponen utama: aplikasi pendaftaran wajah dan aplikasi pengenalan wajah real-time. Dibangun menggunakan Python dengan pustaka `face_recognition` dan `OpenCV`.

## Deskripsi

Sistem ini memungkinkan pengguna untuk mendaftarkan wajah baru ke dalam database dan kemudian mengenali wajah-wajah tersebut melalui kamera secara real-time. Aplikasi ini cocok untuk kebutuhan keamanan, presensi, atau identifikasi personal.

## Fitur

### 1. Pendaftaran Wajah (`face_enrollment_app.py`)

- Menambahkan wajah baru ke sistem dengan nama
- Pengambilan multiple gambar untuk meningkatkan akurasi
- Feedback visual dengan kotak hijau di sekitar wajah terdeteksi
- Validasi untuk memastikan wajah terdeteksi sebelum diambil
- Penyimpanan encoding wajah (bukan gambar) untuk efisiensi penyimpanan
- Deteksi nama duplikat — konfirmasi sebelum menambahkan sampel baru
- Pembatasan interval antar pengambilan gambar (1 detik) untuk menghindari sampel redundan

### 2. Pengenalan Wajah Real-time (`face_recognition_app.py`)

- Pengenalan wajah secara langsung melalui webcam
- Visualisasi dengan kotak warna: hijau untuk wajah yang dikenali, merah untuk yang tidak dikenahi
- Optimasi performa dengan pengolahan setiap frame kedua
- Pencocokan wajah dengan algoritma jarak wajah untuk akurasi yang lebih baik
- Label nama di bawah setiap wajah yang terdeteksi
- Opsi `--tolerance` untuk menyesuaikan ketatnya pencocokan

## Persyaratan

- Python 3.6 atau lebih baru
- Library:
  - `face_recognition`
  - `opencv-python` (cv2)
  - `numpy`

> `dlib` (dibutuhkan `face_recognition`) mungkin memerlukan dependensi sistem tambahan. Pada Windows, gunakan wheel pre-built.

## Instalasi

1. Clone atau download repository ini
2. Install dependensi:

```bash
pip install -r requirements.txt
```

atau secara manual:

```bash
pip install face_recognition opencv-python numpy
```

## Penyimpanan Data

- Encoding wajah disimpan di **`data/known_faces.json`** (format JSON, aman dan dapat dibaca manusia).
- Jika ada data lama dari versi sebelumnya (`data/known_faces_data.pkl`), migrasi otomatis satu kali ke JSON akan berjalan sausage pertama kali aplikasi dijalankan. File pickle lama tidak dihapus agar proses dapat dibalik.
- File `face_data.py` berisi modul persistensi bersama (`load_encodings`, `save_encodings`, `name_exists`) yang dipakai kedua aplikasi.

## Cara Penggunaan

### 1. Pendaftaran Wajah

1. Jalankan aplikasi pendaftaran:

```bash
python face_enrollment_app.py
```

2. Masukkan nama orang yang akan didaftarkan
3. Arahkan wajah ke kamera
4. Tekan tombol `s` untuk mengambil gambar (ambil beberapa gambar dari sudut yang berbeda untuk hasil terbaik)
5. Jika nama sudah terdaftar, sistem akan meminta konfirmasi untuk menambahkan sampel baru
6. Tekan tombol `q` untuk menyelesaikan proses pendaftaran
7. Data encoding wajah akan disimpan ke file `data/known_faces.json`

### 2. Pengenalan Wajah

1. Jalankan aplikasi pengenalan wajah:

```bash
python face_recognition_app.py
```

2. Untuk menyesuaikan sensitivitas (default `0.6`):

```bash
python face_recognition_app.py --tolerance 0.5
```

3. Sistem akan secara otomatis mengenali wajah yang sudah terdaftar:
   - Kotak hijau dengan nama = wajah dikenali
   - Kotak merah dengan label "Tidak Dikenali" = wajah tidak terdaftar
4. Tekan tombol `q` untuk keluar dari aplikasi

Tekan `Ctrl+C` kapan pun untuk keluar dengan aman — kamera akan dilepas otomatis.

## Struktur Direktori

```
face-recognition/
│
├── face_enrollment_app.py  - Aplikasi untuk mendaftarkan wajah
├── face_recognition_app.py - Aplikasi untuk mengenali wajah
├── face_data.py            - Modul persistensi encoding (shared)
├── requirements.txt        - Dependensi Python
├── .gitignore              - Git ignore (env/, data/, __pycache__/)
├── README.md               - Dokumentasi project
│
└── data/
    └── known_faces.json    - File penyimpanan encoding wajah (JSON)
```

## Tips untuk Akurasi Lebih Baik

1. Daftarkan wajah dengan kondisi pencahayaan yang baik
2. Ambil beberapa gambar dari sudut yang berbeda dan dengan ekspresi wajah yang berbeda
3. Untuk mengubah sensitivitas pengenalan, gunakan opsi `--tolerance` (nilai yang lebih rendah = lebih ketat)

## Limitasi

- Kinerja pengenalan wajah bergantung pada kualitas kamera dan pencahayaan
- Diperlukan sumber daya CPU yang cukup untuk pemrosesan real-time
- Untuk jumlah wajah yang sangat banyak, mungkin diperlukan optimasi lebih lanjut

---

Dibuat dengan Python, `face_recognition`, dan OpenCV.
