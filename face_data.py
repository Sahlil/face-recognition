"""Shared face-encoding persistence.

Stores known-face encodings in a JSON file (safe to load untrusted data,
human-readable) instead of a pickle (which is not safe against maliciously
crafted files). Provides automatic one-time migration from the legacy
``known_faces_data.pkl`` if present.
"""
import json
import os
import pickle

import numpy as np

DATA_DIR = "data"
KNOWN_FACES_FILE = os.path.join(DATA_DIR, "known_faces.json")
LEGACY_PKL_FILE = os.path.join(DATA_DIR, "known_faces_data.pkl")


def _migrate_legacy_pickle():
    """One-time migration of the old pickle file into the new JSON format."""
    if os.path.exists(LEGACY_PKL_FILE) and not os.path.exists(KNOWN_FACES_FILE):
        try:
            with open(LEGACY_PKL_FILE, "rb") as f:
                data = pickle.load(f)
            save_encodings(data["encodings"], data["names"])
            print(f"Migrasi otomatis: {LEGACY_PKL_FILE} -> {KNOWN_FACES_FILE}")
            # Keep the old pickle so the migration is reversible.
        except (KeyError, pickle.UnpicklingError, EOFError) as exc:
            print(f"Gagal memigrasi {LEGACY_PKL_FILE}: {exc}. Lanjut dengan data kosong.")


def load_encodings(filename=KNOWN_FACES_FILE):
    """Memuat data encoding wajah yang sudah ada -> (encodings, names)."""
    _migrate_legacy_pickle()
    if not os.path.exists(filename):
        print(f"File data encoding tidak ditemukan: {filename}. Silakan daftar wajah terlebih dahulu.")
        return [], []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"File data rusak ({filename}): {exc}. Lanjut dengan data kosong.")
        return [], []
    encodings = [np.array(e, dtype=np.float64) for e in data.get("encodings", [])]
    names = data.get("names", [])
    return encodings, names


def save_encodings(encodings, names, filename=KNOWN_FACES_FILE):
    """Menyimpan data encoding wajah ke file JSON (format aman)."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = {
        "version": 2,
        "encodings": [e.tolist() if isinstance(e, np.ndarray) else list(e) for e in encodings],
        "names": list(names),
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Data wajah berhasil disimpan ke {filename}")


def name_exists(names, person_name):
    """Memeriksa apakah nama sudah terdaftar (case-insensitive)."""
    return any(n.lower() == person_name.lower() for n in names)
