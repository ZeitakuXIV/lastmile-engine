# Last-Mile Engine

Pipeline simulasi CLI yang membandingkan algoritma Eksak vs Heuristik untuk Last-Mile Delivery di bawah kendala harga BBM dinamis, guna menganalisis Total Cost of Ownership (TCO).

## Anggota Kelompok

| Nama | NPM |
|------|-----|
| Risyam Muhammad Iesqillah | 140810240032 |
| M. Nurrizal Zid Maulana | 140810240054 |
| Joan Clarissa Halimin | 140810240060 |
| Gabriella Marie Keira Wibawa | 140810240086 |

## Cara Menjalankan Program

```bash
# Skenario Subsidi (BBM Rp5.000/L)
python src/main.py --scenario subsidized

# Skenario Krisis (BBM Rp20.000/L)
python src/main.py --scenario crisis

# Kedua skenario
python src/main.py --scenario all

# Dataset kustom
python src/main.py --data data/locations-wide.json --scenario all
```

Tidak ada dependensi pihak ketiga — seluruh algoritma ditulis *from scratch*.

## Dataset

Tiga dataset lokasi real (dataset utama memenuhi syarat minimal 12 pelanggan):

| Dataset | Wilayah | Radius | Jumlah Titik |
|---------|---------|--------|--------------|
| `data/locations.json` | Bandung (urban padat) | ~7 km | 1 hub + 12 pelanggan |
| `data/locations-wide.json` | Jabodetabek (metropolitan) | ~50 km | 1 hub + 12 pelanggan |
| `data/test-n6.json` | Bandung (subset) | ~7 km | 1 hub + 5 pelanggan |

Matriks jarak merepresentasikan jarak jalan (km) antar titik. Berat paket bervariasi 1–6 kg.

## Pemilihan Algoritma

### Algoritma A — Greedy Nearest Neighbor (Heuristik)

Pada setiap langkah, pilih pelanggan terdekat dari posisi saat ini yang belum dikunjungi. Tidak menjamin solusi optimal, tetapi eksekusi sangat cepat (sub-milidetik).

**Trade-off:** Mengorbankan optimalitas jarak demi kecepatan komputasi. Biaya server hampir nol, tetapi biaya BBM lebih tinggi karena rute lebih panjang.

### Algoritma B — Held-Karp DP (Eksak)

Menjamin rute terpendek absolut menggunakan Dynamic Programming dengan *bitmasking*. Menyimpan status kunjungan sebagai bitmask untuk menghindari komputasi ulang subproblem.

**Trade-off:** Menekan biaya BBM lewat rute optimal, tetapi biaya server jauh lebih tinggi. Untuk n=13, eksekusi mencapai ~150–250 ms (vs <0,1 ms greedy).

## Analisis Kompleksitas Big-O

### Greedy Nearest Neighbor

- **Waktu:** O(n²)
  - n iterasi pemilihan titik berikutnya. Setiap iterasi mencari minimum dari (n-i) kandidat.
  - Total: n + (n-1) + ... + 1 = n(n+1)/2
- **Ruang:** O(n)
  - Array `visited` boolean sebesar n + array `path` sebesar n+1.

### Held-Karp DP (Exact)

- **Waktu:** O(n² · 2ⁿ)
  - Subproblem: subset kota (2ⁿ kemungkinan) × kota terakhir (n kemungkinan)
  - Tiap subproblem: iterasi semua kota dalam subset untuk transisi (n)
  - Total operasi: Σ C(n,k) × k × (k-1) = n(n-1) × 2ⁿ⁻²
- **Ruang:** O(n · 2ⁿ)
  - Tabel DP berukuran n × 2ⁿ untuk menyimpan jarak minimum
  - Tabel `parent` berukuran sama untuk rekonstruksi rute

| Algoritma | Waktu | Ruang | Optimal? |
|-----------|-------|-------|----------|
| Greedy NN | O(n²) | O(n) | Tidak |
| Held-Karp DP | O(n²·2ⁿ) | O(n·2ⁿ) | Ya |

## Hasil Eksekusi

### Dataset Bandung (Urban Padat, n=13)

| Metrik | Greedy (Subsidi) | Exact (Subsidi) | Greedy (Krisis) | Exact (Krisis) |
|--------|:----------------:|:----------------:|:----------------:|:----------------:|
| Jarak total | 30,57 km | 23,57 km | 30,57 km | 23,57 km |
| Waktu eksekusi | 0,06 ms | 177,07 ms | 0,05 ms | 164,58 ms |
| Biaya server | Rp3 | Rp8.854 | Rp2 | Rp8.229 |
| Biaya BBM | Rp4.935 | Rp4.312 | Rp19.739 | Rp17.250 |
| **TCO** | **Rp4.938** | **Rp13.166** | **Rp19.741** | **Rp25.479** |
| **Rekomendasi** | ✅ **Greedy** | — | ✅ **Greedy** | — |

### Dataset Jabodetabek (Metropolitan, n=13)

| Metrik | Greedy (Subsidi) | Exact (Subsidi) | Greedy (Krisis) | Exact (Krisis) |
|--------|:----------------:|:----------------:|:----------------:|:----------------:|
| Jarak total | 229 km | 190 km | 229 km | 190 km |
| Waktu eksekusi | 0,10 ms | 236,92 ms | 0,07 ms | 188,50 ms |
| Biaya server | Rp5 | Rp11.846 | Rp4 | Rp9.425 |
| Biaya BBM | Rp34.879 | Rp33.386 | Rp139.514 | Rp133.545 |
| **TCO** | **Rp34.883** | **Rp45.232** | **Rp139.518** | **Rp142.971** |
| **Rekomendasi** | ✅ **Greedy** | — | ✅ **Greedy** | — |

### Dataset n=6 (Bandung subset)

| Metrik | Greedy (Subsidi) | Exact (Subsidi) | Greedy (Krisis) | Exact (Krisis) |
|--------|:----------------:|:----------------:|:----------------:|:----------------:|
| Jarak total | 11,83 km | 11,06 km | 11,83 km | 11,06 km |
| Waktu eksekusi | 0,05 ms | 0,31 ms | 0,02 ms | 0,23 ms |
| Biaya server | Rp2 | **Rp15** | Rp1 | **Rp12** |
| Biaya BBM | Rp1.963 | Rp1.902 | Rp7.852 | Rp7.609 |
| **TCO** | **Rp1.966** | **Rp1.917** | **Rp7.853** | **Rp7.620** |
| **Rekomendasi** | — | ✅ **Exact** | — | ✅ **Exact** |

## Analisis Break-Even

### Cara Hitung

```
Break-Even = ─────────────────────────────────
             Penghematan BBM (liter)
```

### Perhitungan per Dataset

| Dataset | Extra Server | Hemat BBM | Break-Even |
|---------|:-----------:|:---------:|:----------:|
| Bandung n=13 | Rp8.850 | 0,12 L | **Rp71.000/L** |
| Jakarta n=13 | Rp11.800 | 0,30 L | **Rp39.000/L** |
| Bandung n=6 | Rp13 | 0,05 L | **Rp260/L** ✅ |

### Visualisasi

```
Biaya (Rp)  
    ^
    |                  ● Exact (n=13)
    |                 /
    |                /
    |               ● Greedy (n=13)
    |
    |      ● Exact (n=6)
    |     /
    |    ● Greedy (n=6)
    +-------------------------> Harga BBM
          Rp260  Rp71.000
          ↑ BEP n=6    ↑ BEP n=13
```

## Kesimpulan Bisnis

### Skenario Subsidi (BBM Rp5.000/L)

**Rekomendasi: Greedy Nearest Neighbor** untuk n=13. Biaya server exact (~Rp8.800) > penghematan BBM (~Rp600). Untuk n=6, **Exact lebih unggul** karena server cost turun drastis menjadi Rp15.

### Skenario Krisis (BBM Rp20.000/L)

**Rekomendasi: Greedy Nearest Neighbor** untuk n=13. Meskipun penghematan BBM naik jadi ~Rp2.500, masih kalah dari biaya server ~Rp8.800. Untuk n=6, **Exact tetap unggul**.

### Faktor yang Membuat Exact Lebih Layak

1. **Jumlah pelanggan sedikit (n < 10):** Server cost exact turun drastis karena O(n²·2ⁿ). Untuk n=6, server cost cuma Rp15 — 590× lebih murah dari n=13.
2. **Sebaran lokasi sangat luas:** Penghematan BBM membesar seiring selisih jarak greedy vs exact. Break-even turun dari Rp71.000 (Bandung) ke Rp39.000 (Jakarta).
3. **Biaya server lebih murah:** Jika menggunakan komputasi *on-premise* atau server dengan harga lebih rendah dari Rp50/ms.

### Rekomendasi Final

Perusahaan sebaiknya **tetap menggunakan algoritma Greedy** untuk operasional *last-mile delivery* pada kondisi normal (n=13). Investasi pada algoritma eksak hanya layak jika harga BBM melampaui Rp39.000/L, jumlah pelanggan per rute kurang dari 10, atau biaya server dapat ditekan secara signifikan.
