import face_recognition
import cv2
import os
import numpy as np
import pickle

# Direktori untuk menyimpan data encoding
DATA_DIR = "data"
KNOWN_FACES_DATA_FILE = os.path.join(DATA_DIR, "known_faces_data.pkl")

def load_encodings(filename=KNOWN_FACES_DATA_FILE):
    """Memuat data encoding wajah yang sudah ada."""
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
            return data["encodings"], data["names"]
    print(f"File data encoding tidak ditemukan: {filename}. Silakan daftar wajah terlebih dahulu.")
    return [], []

def run_face_recognition_app():
    """Menjalankan aplikasi pengenalan wajah secara real-time."""
    known_face_encodings, known_face_names = load_encodings()

    if not known_face_encodings:
        print("Tidak ada wajah yang terdaftar. Silakan jalankan 'face_enrollment_app.py' terlebih dahulu untuk mendaftarkan wajah.")
        return

    video_capture = cv2.VideoCapture(0) # Menggunakan kamera webcam
    if not video_capture.isOpened():
        print("Error: Tidak dapat membuka kamera.")
        return

    # Variabel untuk menghemat sumber daya CPU
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    print("Memulai pengenalan wajah. Tekan 'q' untuk keluar.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break

        # Ubah ukuran frame untuk pemrosesan lebih cepat (opsional, tapi disarankan)
        # Scaling down by 1/4 makes it 4x faster.
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Ubah gambar dari BGR (OpenCV) ke RGB (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        if process_this_frame:
            # Temukan semua wajah dan encoding wajah di frame saat ini
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # Bandingkan wajah di frame dengan wajah yang dikenal
                # tolerance=0.6 adalah ambang batas umum. Angka lebih kecil = lebih ketat.
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Tidak Dikenal"

                # Gunakan jarak wajah untuk menemukan kecocokan terbaik (yang paling mirip)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                # Jika ada kecocokan dan jaraknya di bawah ambang batas toleransi
                if matches[best_match_index]: # and face_distances[best_match_index] < 0.5: # Bisa tambahkan threshold di sini juga
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame # Proses setiap frame lainnya untuk efisiensi

        # Tampilkan hasil di frame asli (skalakan kembali lokasi wajah)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Gambar kotak di sekitar wajah
            color = (0, 255, 0) if name != "Tidak Dikenal" else (0, 0, 255) # Hijau jika dikenal, Merah jika tidak
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Gambar label dengan nama di bawah wajah
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Tampilkan frame hasil
        cv2.imshow('Face Recognition', frame)

        # Tekan 'q' untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Aplikasi pengenalan wajah ditutup.")

if __name__ == "__main__":
    run_face_recognition_app()