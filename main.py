import os
import time
from math import gcd

# ==============================================================================
# KONFIGURASI FOLDER OUTPUT
# ==============================================================================
# Folder ini digunakan untuk menyimpan file hasil enkripsi (ciphertext)
OUTPUT_FOLDER = "hasil_enkripsi"

# Jika folder belum ada, maka akan dibuat otomatis
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ==============================================================================
# METODE 1 – PRNG (Linear Congruential Generator / LCG)
# ==============================================================================
def lcg_generator(seed, n):
    """
    Fungsi ini menghasilkan deretan bilangan pseudo-random
    menggunakan algoritma Linear Congruential Generator (LCG).

    seed : nilai awal pembangkit acak
    n    : jumlah bilangan acak yang dihasilkan
    """
    a = 1103515245   # konstanta pengali
    c = 12345        # konstanta penambah
    m = 256          # modulus (disesuaikan dengan ASCII)

    x = seed         # nilai awal
    # Menghasilkan n bilangan pseudo-random
    return [(x := (a * x + c) % m) for _ in range(n)]

# ==============================================================================
# METODE 2 – AFFINE CIPHER
# ==============================================================================
def mod_inverse(a, m=256):
    """
    Mencari invers modulo dari nilai a.
    Digunakan saat proses dekripsi Affine Cipher.
    """
    for i in range(m):
        if (a * i) % m == 1:
            return i
    raise ValueError("Tidak ada invers modulo")

def affine_encrypt(text, a, b):
    """
    Melakukan enkripsi Affine Cipher.
    Setiap karakter diubah menjadi karakter baru
    berdasarkan kunci a dan b.
    """
    return ''.join(chr((a * ord(c) + b) % 256) for c in text)

def affine_decrypt(text, a, b):
    """
    Melakukan dekripsi Affine Cipher.
    Proses ini membalik enkripsi Affine menggunakan invers modulo.
    """
    a_inv = mod_inverse(a)
    return ''.join(chr((a_inv * (ord(c) - b)) % 256) for c in text)

# ==============================================================================
# METODE 3 – CHAOTIC PERMUTATION (LOGISTIC MAP)
# ==============================================================================
def logistic_map(a, x0, n):
    """
    Menghasilkan deretan nilai chaos menggunakan Logistic Map.
    Nilai ini digunakan untuk menentukan urutan permutasi karakter.
    """
    x = x0
    chaos = []
    for _ in range(n):
        x = a * x * (1 - x)
        chaos.append(x)
    return chaos

def get_permutation_indices(chaos):
    """
    Menghasilkan indeks permutasi berdasarkan urutan nilai chaos.
    Karakter akan diacak berdasarkan indeks ini.
    """
    return [i for i, _ in sorted(enumerate(chaos), key=lambda x: x[1])]

def apply_permutation(text, idx):
    """
    Mengacak posisi karakter berdasarkan indeks permutasi.
    """
    return ''.join(text[i] for i in idx)

def inverse_permutation(text, idx):
    """
    Mengembalikan posisi karakter ke urutan semula
    (digunakan saat dekripsi).
    """
    res = [''] * len(text)
    for i, j in enumerate(idx):
        res[j] = text[i]
    return ''.join(res)

# ==============================================================================
# INPUT KUNCI DARI PENGGUNA
# ==============================================================================
def input_kunci():
    """
    Mengambil seluruh kunci yang dibutuhkan dari pengguna.
    Disertai nilai default agar mudah diuji.
    """
    try:
        seed = int(input("   Seed PRNG (default 123): ") or 123)
        a_aff = int(input("   a Affine (default 5): ") or 5)
        b_aff = int(input("   b Affine (default 8): ") or 8)
        chaos_a = float(input("   Chaos a (default 3.9): ") or 3.9)
        x0 = float(input("   x0 (default 0.5): ") or 0.5)

        # Validasi kunci Affine
        if gcd(a_aff, 256) != 1:
            raise ValueError("a tidak relatif prima")

        return seed, a_aff, b_aff, chaos_a, x0
    except:
        return None

# ==============================================================================
# PROSES ENKRIPSI
# ==============================================================================
def enkripsi():
    """
    Proses enkripsi utama:
    1. PRNG XOR
    2. Affine Cipher
    3. Chaotic Permutation
    """
    plaintext = input("\nMasukkan teks: ")
    kunci = input_kunci()
    if not kunci:
        print("Kunci tidak valid")
        return

    seed, a_aff, b_aff, chaos_a, x0 = kunci
    n = len(plaintext)

    # Tahap 1: Substitusi menggunakan PRNG XOR
    prng = lcg_generator(seed, n)
    step1 = ''.join(chr(ord(plaintext[i]) ^ prng[i]) for i in range(n))

    # Tahap 2: Substitusi menggunakan Affine Cipher
    step2 = affine_encrypt(step1, a_aff, b_aff)

    # Tahap 3: Mutasi posisi karakter menggunakan chaos
    chaos = logistic_map(chaos_a, x0, n)
    idx = get_permutation_indices(chaos)
    cipher = apply_permutation(step2, idx)

    # Simpan ciphertext ke file
    with open(os.path.join(OUTPUT_FOLDER, "cipher.bin"), "wb") as f:
        f.write(bytearray(ord(c) for c in cipher))

    print("\n[OK] Enkripsi selesai")

# ==============================================================================
# PROSES DEKRIPSI
# ==============================================================================
def dekripsi():
    """
    Proses dekripsi:
    1. Inverse Chaotic Permutation
    2. Dekripsi Affine
    3. PRNG XOR
    """
    with open(os.path.join(OUTPUT_FOLDER, "cipher.bin"), "rb") as f:
        cipher = ''.join(chr(b) for b in f.read())

    kunci = input_kunci()
    if not kunci:
        return

    seed, a_aff, b_aff, chaos_a, x0 = kunci
    n = len(cipher)

    # Tahap 1: Kembalikan posisi karakter
    chaos = logistic_map(chaos_a, x0, n)
    idx = get_permutation_indices(chaos)
    step1 = inverse_permutation(cipher, idx)

    # Tahap 2: Dekripsi Affine
    step2 = affine_decrypt(step1, a_aff, b_aff)

    # Tahap 3: XOR PRNG
    prng = lcg_generator(seed, n)
    plaintext = ''.join(chr(ord(step2[i]) ^ prng[i]) for i in range(n))

    print("\nHASIL DEKRIPSI:", plaintext)

# ==============================================================================
# PROGRAM UTAMA (MENU)
# ==============================================================================
def main():
    """
    Menu utama program.
    """
    while True:
        print("\n1. Enkripsi\n2. Dekripsi\n3. Keluar")
        p = input("Pilih: ")
        if p == '1':
            enkripsi()
        elif p == '2':
            dekripsi()
        elif p == '3':
            break

# Menjalankan program
if __name__ == "__main__":
    main()
