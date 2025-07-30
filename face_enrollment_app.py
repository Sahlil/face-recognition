import cv2
import os
import time
import face_recognition
import pickle

# Direktori untuk menyimpan data encoding dan gambar sementara
DATA_DIR = "data"
KNOWN_FACES_DATA_FILE = os.path.join(DATA_DIR, "known_faces_data.pkl")

def load_encodings(filename=KNOWN_FACES_DATA_FILE):
    """Memuat data encoding wajah yang sudah ada."""
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            return data["encodings"], data["names"]
    return [], []

def save_encodings(encodings, names, filename=KNOWN_FACES_DATA_FILE):
    """Menyimpan data encoding wajah."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = {"encodings": encodings, "names": names}
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
    print(f"Data wajah berhasil disimpan ke {filename}")

def enroll_new_face():
    """Mengelola proses pendaftaran wajah baru."""
    person_name = input("Masukkan nama orang baru (contoh: John Doe): ").strip()
    if not person_name:
        print("Nama tidak boleh kosong. Pembatalan pendaftaran.")
        return

    print(f"\nMemulai pendaftaran untuk: {person_name}")
    print("Arahkan wajah Anda ke kamera.")
    print("Tekan 's' untuk mengambil gambar.")
    print("Tekan 'q' untuk selesai/keluar.")
    print("Ambil beberapa gambar dari berbagai sudut dan ekspresi untuk akurasi yang lebih baik.")

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Tidak dapat membuka kamera.")
        return

    captured_images = []
    img_count = 0
    last_capture_time = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break

        # Deteksi wajah di frame untuk feedback visual
        face_locations = face_recognition.face_locations(frame)
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2) # Hijau untuk wajah terdeteksi
            cv2.putText(frame, "Wajah Terdeteksi", (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)

        cv2.imshow('Pendaftaran Wajah Baru', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            current_time = time.time()
            # Batasi pengambilan gambar per detik
            if current_time - last_capture_time > 1.0:
                if face_locations: # Pastikan ada wajah terdeteksi sebelum menyimpan
                    captured_images.append(frame)
                    img_count += 1
                    print(f"Gambar {img_count} berhasil diambil.")
                    last_capture_time = current_time
                else:
                    print("Tidak ada wajah terdeteksi. Pastikan wajah Anda di dalam frame.")
            else:
                print("Terlalu cepat! Tunggu sebentar sebelum mengambil gambar lagi.")
        elif key == ord('q'):
            print("Pengambilan gambar selesai.")
            break

    video_capture.release()
    cv2.destroyAllWindows()

    if not captured_images:
        print("Tidak ada gambar yang diambil. Pendaftaran dibatalkan.")
        return

    print(f"Menghitung encoding untuk {len(captured_images)} gambar...")
    new_face_encodings = []
    for i, img in enumerate(captured_images):
        # Ubah gambar dari BGR (OpenCV) ke RGB (face_recognition)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_img)
        if encodings:
            new_face_encodings.append(encodings[0])
        else:
            print(f"Peringatan: Tidak ada wajah terdeteksi di gambar yang diambil ke-{i+1}.")

    if not new_face_encodings:
        print("Tidak ada encoding wajah yang dapat dihitung dari gambar yang diambil. Pendaftaran gagal.")
        return

    # Muat data yang sudah ada
    known_encodings, known_names = load_encodings()

    # Tambahkan encoding baru dan nama ke daftar
    for enc in new_face_encodings:
        known_encodings.append(enc)
        known_names.append(person_name)

    # Simpan kembali data yang diperbarui
    save_encodings(known_encodings, known_names)
    print(f"Wajah '{person_name}' dengan {len(new_face_encodings)} sampel telah berhasil didaftarkan.")

if __name__ == "__main__":
    enroll_new_face()