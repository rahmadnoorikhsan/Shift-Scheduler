# Shift Scheduler — Technical Support

Web app jadwal shift dengan reshuffle otomatis berbasis GitHub Pages + Actions.

## Struktur repo

```
.
├── .github/
│   └── workflows/
│       └── reshuffle.yml   # Workflow reshuffle
├── docs/
│   ├── index.html          # Web app (GitHub Pages)
│   └── state.json          # State siklus aktif
└── reshuffle.py            # Script Python reshuffle + constraint
```

## Setup awal

### 1. Aktifkan GitHub Pages
1. Buka repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: `/docs`
4. Klik **Save** — URL akan muncul dalam ~1 menit

### 2. Pastikan Actions punya write permission
1. **Settings** → **Actions** → **General**
2. Scroll ke *Workflow permissions* → pilih **Read and write permissions**
3. Klik **Save**

## Cara reshuffle

### Manual (rekomendasi — dilakukan tiap akhir Minggu ke-5)
1. Buka tab **Actions** di repo
2. Pilih workflow **Reshuffle Jadwal Shift**
3. Klik **Run workflow**
4. Isi kolom konfirmasi dengan `reshuffle`
5. Klik **Run workflow** (hijau)

Setelah ~1 menit, `docs/state.json` otomatis diupdate dan halaman web langsung reflect urutan baru.

### Otomatis (opsional)
Workflow sudah dikonfigurasi cron tiap **Minggu malam 23:00 WIB**.
Jika ingin auto-reshuffle tiap 5 minggu sekali, tambahkan logika pengecekan siklus di `reshuffle.py`.

## Constraint yang dijaga otomatis

Aturannya berbasis **seat (posisi), bukan nama**: siapa pun yang menempati seat yang
masih bertugas di hari **Minggu Week 5** tidak boleh ganti tipe shift pada hari
**Senin Week 1** tanpa libur di antaranya.
- Berakhir **S1** (Minggu W5) → Senin W1 berikutnya harus **S1 atau LIBUR**
- Berakhir **S2** (Minggu W5) → Senin W1 berikutnya harus **S2 atau LIBUR**
- Berakhir **LIBUR** → bebas pindah ke seat mana saja

Pada siklus saat ini, seat yang bertugas hari Minggu W5 adalah seat 1 (**Aji**, S1) dan
seat 2 (**Djaloe**, S2), jadi merekalah yang terikat constraint. Setelah diacak,
constraint otomatis mengikuti siapa pun yang menempati seat tersebut.

Script mencoba hingga 10.000 kombinasi acak hingga constraint terpenuhi.
