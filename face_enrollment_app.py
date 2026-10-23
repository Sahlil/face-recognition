import cv2
import face_recognition
import sys

import face_data


def enroll_new_face():
    """Mengelola proses pendaftaran wajah baru."""
    person_name = input("Masukkan nama orang baru (contoh: John Doe): ").strip()
    if not person_name:
        print("Nama tidak boleh kosong. Pembatalan pendaftaran.")
        return

    known_encodings, known_names = face_data.load_encodings()
    if face_data.name_exists(known_names, person_name):
        choice = input(
            f"Peringatan: '{person_name}' sudah terdaftar "
            f"({known_names.count([n for n in known_names if n.lower() == person_name.lower()][0])} sampel). "
            "Tambahkan sampel lagi? [y/N]: "
        ).strip().lower()
        if choice != "y":
            print("Pembatalan pendaftaran.")
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

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Gagal membaca frame dari kamera.")
                break

            # Resize kecil untuk deteksi yang konsisten dan cepat (sama seperti recognition app)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame)

            # Deteksi di frame kecil; kotak harus diskala 4x untuk ditampilkan di frame asli
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 255, 0), 2)
                cv2.putText(frame, "Wajah Terdeteksi", (left * 4 + 6, top * 4 - 6),
                            cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)

            cv2.imshow('Pendaftaran Wajah Baru', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                import time
                current_time = time.time()
                if current_time - last_capture_time > 1.0:
                    if face_locations:
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
    finally:
        video_capture.release()
        cv2.destroyAllWindows()

    if not captured_images:
        print("Tidak ada gambar yang diambil. Pendaftaran dibatalkan.")
        return

    print(f"Menghitung encoding untuk {len(captured_images)} gambar...")
    new_face_encodings = []
    for i, img in enumerate(captured_images):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_img)
        if encodings:
            new_face_encodings.append(encodings[0])
        else:
            print(f"Peringatan: Tidak ada wajah terdeteksi di gambar yang diambil ke-{i+1}.")

    if not new_face_encodings:
        print("Tidak ada encoding wajah yang dapat dihitung dari gambar yang diambil. Pendaftaran gagal.")
        return

    # Tambahkan encoding baru dan nama ke daftar
    for enc in new_face_encodings:
        known_encodings.append(enc)
        known_names.append(person_name)

    face_data.save_encodings(known_encodings, known_names)
    print(f"Wajah '{person_name}' dengan {len(new_face_encodings)} sampel telah berhasil didaftarkan.")


if __name__ == "__main__":
    try:
        enroll_new_face()
    except KeyboardInterrupt:
        sys.exit("\nPendaftaran dibatalkan.\n")
