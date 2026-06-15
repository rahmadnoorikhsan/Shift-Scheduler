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

Saat reshuffle, script memastikan:
- **Djaloe**: Shift Minggu terakhir (S2/LIBUR) → Shift Senin pertama siklus baru (S2/LIBUR) — tidak lompat ke S1
- **Aji**: Shift Minggu terakhir (S1/LIBUR) → Shift Senin pertama siklus baru (S1/LIBUR) — tidak lompat ke S2

Script mencoba hingga 10.000 kombinasi acak hingga constraint terpenuhi.
