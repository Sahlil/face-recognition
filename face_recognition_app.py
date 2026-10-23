import argparse
import cv2
import face_recognition
import numpy as np
import sys

import face_data

DEFAULT_TOLERANCE = 0.6


def run_face_recognition_app(tolerance=DEFAULT_TOLERANCE):
    """Menjalankan aplikasi pengenalan wajah secara real-time."""
    known_face_encodings, known_face_names = face_data.load_encodings()

    if not known_face_encodings:
        print("Tidak ada wajah yang terdaftar. Silakan jalankan 'face_enrollment_app.py' terlebih dahulu.")
        return

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Tidak dapat membuka kamera.")
        return

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    print("Memulai pengenalan wajah. Tekan 'q' untuk keluar.")

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Gagal membaca frame dari kamera.")
                break

            # Scaling down by 1/4 makes it 4x faster.
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    name = "Tidak Dikenal"
                    # Gunakan jarak wajah ke semua wajah dikenal; kecocokan terdekat menang.
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = int(np.argmin(face_distances))
                    if face_distances[best_match_index] <= tolerance:
                        name = known_face_names[best_match_index]
                    face_names.append(name)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                color = (0, 255, 0) if name != "Tidak Dikenal" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video_capture.release()
        cv2.destroyAllWindows()
    print("Aplikasi pengenakan wajah ditutup.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aplikasi pengenalan wajah real-time")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE,
                        help=f"Ambang ketatnya pencocokan (default {DEFAULT_TOLERANCE}). Lebih kecil = lebih ketat.")
    args = parser.parse_args()
    try:
        run_face_recognition_app(tolerance=args.tolerance)
    except KeyboardInterrupt:
        sys.exit("\nAplikasi ditutup.\n")
