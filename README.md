1. PRNG (Pseudo Random Number Generator – LCG)

Metode pertama yang digunakan adalah PRNG dengan algoritma Linear Congruential Generator.

PRNG ini berfungsi untuk menghasilkan bilangan acak semu yang kemudian digunakan sebagai kunci sementara. Setiap karakter plaintext diubah menggunakan operasi XOR dengan bilangan acak tersebut.

Tujuan penggunaan PRNG adalah untuk menghilangkan pola karakter asli sehingga teks tidak bisa dianalisis menggunakan analisis frekuensi.

Metode ini memenuhi syarat pseudo-random substitution karena kunci yang digunakan bersifat acak dan bergantung pada seed awal.

2. Substitusi Menggunakan Affine Cipher

Setelah proses PRNG, hasil teks kemudian diproses menggunakan Affine Cipher, yaitu metode substitusi klasik.

Pada tahap ini, setiap karakter diubah berdasarkan perhitungan matematis sederhana sehingga nilai karakter menjadi berbeda dari sebelumnya.

Fungsi utama Affine Cipher adalah untuk menambah lapisan substitusi kedua, sehingga meskipun hasil PRNG berhasil ditebak, data tetap tidak bisa langsung dikembalikan ke bentuk semula.

Penggunaan Affine Cipher juga bertujuan untuk mengombinasikan metode kriptografi klasik dan modern dalam satu sistem.

3. Chaotic System Menggunakan Logistic Map

Metode ketiga adalah Chaotic System dengan Logistic Map.

Chaotic system digunakan untuk menghasilkan deret nilai yang sangat sensitif terhadap nilai awal. Perubahan kecil pada kunci akan menghasilkan urutan yang sangat berbeda.

Dalam program ini, chaotic system tidak digunakan untuk substitusi, melainkan untuk mengacak posisi karakter.

4. Permutasi Karakter Berbasis Chaos

Nilai chaos yang dihasilkan kemudian digunakan untuk menentukan urutan permutasi karakter.

Dengan permutasi ini, posisi karakter dalam teks diacak sehingga struktur asli teks benar-benar hilang.

Tujuan permutasi adalah untuk memberikan diffusion, yaitu menyebarkan perubahan satu karakter ke seluruh posisi teks.
