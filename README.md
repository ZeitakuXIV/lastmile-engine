# Last-Mile Engine

Pipeline simulasi CLI yang membandingkan algoritma Eksak vs Heuristik untuk Last-Mile Delivery di bawah kendala harga BBM dinamis, guna menganalisis Total Cost of Ownership (TCO).

## Anggota Kelompok

| Nama | NPM |
|------|-----|
| Risyam Muhammad Iesqillah | 140810240032 |
| M. Nurrizal Zid Maulana | 140810240054 |
| Joan Clarissa Halimin | 140810240060 |
| Gabriella Marie Keira Wibawa | 140810240086 |

## How to Run

```bash
python src/main.py --scenario subsidized    # BBM Rp5.000/L
python src/main.py --scenario crisis        # BBM Rp20.000/L
python src/main.py --all                    # dua skenario
```

## Struktur Folder

```
├── src/           # Source code Python
├── data/          # Dataset lokasi dan matriks jarak
├── docs/          # Screenshot output
├── .gitignore
└── README.md
```
