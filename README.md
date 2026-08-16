# Aplikasi Pengenalan Wajah (Face Recognition App)

Aplikasi ini adalah sistem pengenalan wajah sederhana yang terdiri dari dua komponen utama: aplikasi pendaftaran wajah dan aplikasi pengenalan wajah real-time. Dibangun menggunakan Python dengan pustaka face_recognition dan OpenCV.

## Deskripsi

Sistem ini memungkinkan pengguna untuk mendaftarkan wajah baru ke dalam database dan kemudian mengenali wajah-wajah tersebut melalui kamera secara real-time. Aplikasi ini cocok untuk kebutuhan keamanan, presensi, atau identifikasi personal.

## Fitur

### 1. Pendaftaran Wajah (`face_enrollment_app.py`)

- Menambahkan wajah baru ke sistem dengan nama
- Pengambilan multiple gambar untuk meningkatkan akurasi
- Feedback visual dengan kotak hijau di sekitar wajah terdeteksi
- Validasi untuk memastikan wajah terdeteksi sebelum diambil
- Penyimpanan encoding wajah (bukan gambar) untuk efisiensi penyimpanan

### 2. Pengenalan Wajah Real-time (`face_recognition_app.py`)

- Pengenalan wajah secara langsung melalui webcam
- Visualisasi dengan kotak warna: hijau untuk wajah yang dikenali, merah untuk yang tidak dikenali
- Optimasi performa dengan pengolahan setiap frame kedua
- Pencocokan wajah dengan algoritma jarak wajah untuk akurasi yang lebih baik
- Label nama di bawah setiap wajah yang terdeteksi

## Persyaratan

- Python 3.6 atau lebih baru
- Library:
  - face_recognition
  - opencv-python (cv2)
  - numpy
  - pickle

## Instalasi

1. Clone atau download repository ini
2. Install library yang dibutuhkan:

```bash
pip install face_recognition opencv-python numpy
```

> **Catatan**: Library `face_recognition` membutuhkan `dlib` yang mungkin memerlukan beberapa dependensi sistem tambahan. Pada Windows, disarankan untuk menginstall wheel file yang pre-built.

## Cara Penggunaan

### 1. Pendaftaran Wajah

1. Jalankan aplikasi pendaftaran:

```bash
python face_enrollment_app.py
```

2. Masukkan nama orang yang akan didaftarkan
3. Arahkan wajah ke kamera
4. Tekan tombol `s` untuk mengambil gambar (ambil beberapa gambar dari sudut yang berbeda untuk hasil terbaik)
5. Tekan tombol `q` untuk menyelesaikan proses pendaftaran
6. Data encoding wajah akan disimpan ke file `data/known_faces_data.pkl`

### 2. Pengenalan Wajah

1. Jalankan aplikasi pengenalan wajah:

```bash
python face_recognition_app.py
```

2. Sistem akan secara otomatis mengenali wajah yang sudah terdaftar:
   - Kotak hijau dengan nama = wajah dikenali
   - Kotak merah dengan label "Tidak Dikenal" = wajah tidak terdaftar
3. Tekan tombol `q` untuk keluar dari aplikasi

## Struktur Direktori

```
face-recognition/
│
├── face_enrollment_app.py  - Aplikasi untuk mendaftarkan wajah
├── face_recognition_app.py - Aplikasi untuk mengenali wajah
├── README.md               - Dokumentasi project
│
└── data/
    └── known_faces_data.pkl - File penyimpanan encoding wajah
```

## Tips untuk Akurasi Lebih Baik

1. Daftarkan wajah dengan kondisi pencahayaan yang baik
2. Ambil beberapa gambar dari sudut yang berbeda dan dengan ekspresi wajah yang berbeda
3. Untuk mengubah sensitivitas pengenalan, sesuaikan nilai `tolerance` di file `face_recognition_app.py` (nilai yang lebih rendah = lebih ketat)

## Limitasi

- Kinerja pengenalan wajah bergantung pada kualitas kamera dan pencahayaan
- Diperlukan sumber daya CPU yang cukup untuk pemrosesan real-time
- Untuk jumlah wajah yang sangat banyak, mungkin diperlukan optimasi lebih lanjut

---

Dibuat dengan Python, face_recognition, dan OpenCV.
