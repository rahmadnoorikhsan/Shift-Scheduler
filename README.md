# Shift Scheduler — Technical Support

Web app jadwal shift tim Technical Support (5 orang) dengan **reshuffle otomatis tiap
5 minggu** di bawah aturan keadilan. Tanpa backend, tanpa database — hanya halaman
statis di **GitHub Pages** + satu script Python yang dijalankan **GitHub Actions**.

🔗 **Live:** https://rahmadnoorikhsan.github.io/Shift-Scheduler/

---

## Daftar isi
1. [Konsep singkat](#1-konsep-singkat)
2. [Jenis shift](#2-jenis-shift)
3. [Aturan jadwal (rules)](#3-aturan-jadwal-rules)
4. [Mekanisme keseluruhan](#4-mekanisme-keseluruhan)
5. [Reshuffle & constraint](#5-reshuffle--constraint)
6. [Struktur repo](#6-struktur-repo)
7. [Operasional sehari-hari](#7-operasional-sehari-hari)
8. [Cara mengubah data](#8-cara-mengubah-data)
9. [Catatan penting (gotcha)](#9-catatan-penting-gotcha)

---

## 1. Konsep singkat

- Jadwal disusun untuk **1 siklus = 5 minggu**.
- Jadwal **tidak terikat ke nama orang**, tapi ke **posisi/seat (0–4)**. Pola shift
  sudah baku per posisi; siapa yang menempati posisi mana ditentukan oleh urutan
  (`order`) di `docs/state.json`.
- Setiap akhir siklus (5 minggu), **orang-orangnya diacak ulang** ke posisi baru
  (reshuffle) supaya beban shift bergilir adil — pola posisinya tetap, yang berputar
  adalah penempatan orangnya.

---

## 2. Jenis shift

| Kode | Arti | Jam |
|---|---|---|
| `S1` | Shift pagi | 06:00–14:00 |
| `S2` | Shift sore/malam | 13:00–21:00 |
| `LIBUR` | Hari libur | — |

`S1` dan `S2` sengaja **tumpang-tindih 13:00–14:00**, sehingga cakupan layanan penuh
**06:00–21:00** ("full coverage").

---

## 3. Aturan jadwal (rules)

1. **Pola tetap per posisi.** Ada matriks baku `PATTERN[posisi][minggu][hari]`:
   - `posisi`: 0–4 (seat dalam rotasi)
   - `minggu`: 0–4 (Minggu 1–5)
   - `hari`: 0–6 (Senin … Minggu)

   Setiap sel berisi `S1`, `S2`, atau `LIBUR`. Sumber kebenaran pola ini adalah sheet
   *"Shift Weekend Coverage (5P)"* pada `JADWAL SHIFT TS FULL COVERAGE.xlsx`.

2. **Rotasi bertahap (staggered).** Pola dibangun dari **5 arketipe mingguan** R1–R5.
   Tiap posisi menjalani kelima arketipe itu, hanya digeser fasenya satu minggu:

   | Arketipe | Sen–Min |
   |---|---|
   | R1 | `S1 S1 S1 S1 LIBUR S2 LIBUR` |
   | R2 | `LIBUR S1 S1 S1 S1 S1 LIBUR` |
   | R3 | `S1 LIBUR S2 S2 S2 S2 LIBUR` |
   | R4 | `S2 S2 LIBUR S2 S2 LIBUR S2` |
   | R5 | `S2 S2 S2 LIBUR S1 LIBUR S1` |

   | Posisi | Mgg 1 | Mgg 2 | Mgg 3 | Mgg 4 | Mgg 5 |
   |---|---|---|---|---|---|
   | 0 | R5 | R1 | R2 | R3 | R4 |
   | 1 | R1 | R2 | R3 | R4 | R5 |
   | 2 | R2 | R3 | R4 | R5 | R1 |
   | 3 | R3 | R4 | R5 | R1 | R2 |
   | 4 | R4 | R5 | R1 | R2 | R3 |

3. **Adil & menutup semua hari.** Karena setiap posisi menjalani kelima arketipe,
   dalam satu siklus tiap posisi mendapat campuran seimbang minggu pagi, sore, dan
   libur — dan tim secara kolektif menutup semua hari.

4. **Keadilan antar-orang dijaga lewat reshuffle**, bukan dengan mengubah pola. Lihat
   [§5](#5-reshuffle--constraint).

5. **Constraint kontinuitas shift** saat pergantian siklus — lihat [§5](#5-reshuffle--constraint).

> Aturan operasional manusia (backup saat sakit, tukar shift, poin libur nasional)
> ada di SOP terpisah (sheet *"SOP Manajemen Shift"*) dan **tidak** ditegakkan oleh
> kode — itu proses tim, bukan logika aplikasi.

---

## 4. Mekanisme keseluruhan

```
                    ┌──────────────────────────────────────────┐
                    │  docs/state.json  (sumber kebenaran state) │
                    │  cycle, order[], history[], last_reshuffled│
                    └───────────────┬───────────────┬───────────┘
                                    │ dibaca         │ ditulis
                          (runtime) │                │ (saat reshuffle)
                                    ▼                │
        ┌──────────────────────────────────┐        │
        │ docs/index.html  (GitHub Pages)   │        │
        │ baca state.json + PATTERN →       │        │
        │ render tabel jadwal di browser    │        │
        └──────────────────────────────────┘        │
                                                     │
        ┌────────────────────────────────────────────┴───────────┐
        │ reshuffle.py  (dijalankan GitHub Actions)                │
        │ acak order[] dgn constraint → cycle++ →                  │
        │ commit & push state.json baru ke main                    │
        └──────────────────────────────────────────────────────────┘
```

Alur:
1. **Tampilan.** Browser membuka `index.html` (di GitHub Pages), yang membaca
   `state.json` saat runtime, lalu memetakan `order[posisi] → orang` dan menggambar
   shift dari `PATTERN`.
2. **Pergantian siklus.** Workflow Actions menjalankan `reshuffle.py`, yang mengacak
   `order`, menambah `cycle`, mencatat ke `history`, lalu **commit + push**
   `state.json` kembali ke `main`.
3. **Auto-deploy.** Push ke `main` memicu GitHub Pages me-redeploy `docs/` otomatis —
   halaman langsung menampilkan urutan baru (~1 menit).

State saat ini (`docs/state.json`):
```json
{ "cycle": 1, "order": ["Djaloe", "Aji", "Dimas", "Fazri", "Faza"] }
```
Artinya: Djaloe = posisi 0, Aji = posisi 1, Dimas = posisi 2, Fazri = posisi 3,
Faza = posisi 4.

---

## 5. Reshuffle & constraint

**Tujuan:** menggilir siapa menempati posisi mana di siklus berikutnya, supaya beban
pagi/sore/libur bergilir adil antar-orang.

**Cara kerja `reshuffle.py`:**
1. Acak `order` (permutasi baru, tidak boleh identik dengan yang lama).
2. Pastikan **constraint kontinuitas shift** terpenuhi (lihat di bawah).
3. Coba sampai **10.000 kali**; jika tetap gagal → error.
4. Jika berhasil: `cycle += 1`, simpan `order` baru, append ke `history`, set
   `last_reshuffled`.

**Constraint kontinuitas shift (berbasis SEAT, bukan nama):**
Siapa pun yang menempati seat yang **masih bertugas di Minggu (hari) Week 5** tidak
boleh berganti tipe shift pada **Senin Week 1** siklus berikutnya tanpa libur di
antaranya:

- Berakhir **S1** di Minggu W5 → Senin W1 berikutnya harus **S1 atau LIBUR**
- Berakhir **S2** di Minggu W5 → Senin W1 berikutnya harus **S2 atau LIBUR**
- Berakhir **LIBUR** di Minggu W5 → **bebas** pindah ke posisi mana saja

Constraint mengikuti **seat**, jadi otomatis berlaku ke siapa pun yang nanti menempati
seat tersebut — tidak ada nama yang di-hardcode.

---

## 6. Struktur repo

```
reshuffle.py                     # Algoritma reshuffle + constraint (entry point)
docs/
  index.html                     # Web app (vanilla JS, tanpa framework)
  state.json                     # Sumber kebenaran: cycle + order + history
.github/workflows/reshuffle.yml  # Workflow manual/cron yang menjalankan reshuffle.py
README.md                        # Dokumen ini
wiki/                            # Basis pengetahuan (dikelola agen LLM)
CLAUDE.md                        # Panduan untuk agen LLM
```

---

## 7. Operasional sehari-hari

### Reshuffle manual (rekomendasi — tiap akhir Minggu ke-5)
1. Buka tab **Actions** di repo
2. Pilih workflow **Reshuffle Jadwal Shift**
3. Klik **Run workflow**
4. Isi kolom konfirmasi dengan `reshuffle`
5. Klik **Run workflow** (hijau)

Setelah ~1 menit `docs/state.json` terupdate otomatis dan halaman web mengikuti.

### Reshuffle otomatis (cron)
Workflow sudah dijadwalkan cron tiap **Minggu malam 23:00 WIB** (16:00 UTC). Saat ini
cron akan reshuffle setiap kali jalan; jika ingin benar-benar hanya tiap 5 minggu,
tambahkan pengecekan siklus/tanggal di `reshuffle.py`.

### Preview lokal
```bash
python3 reshuffle.py            # Jalankan reshuffle lokal (mengubah docs/state.json)
python3 -m http.server -d docs  # Preview web app di http://localhost:8000
```

---

## 8. Cara mengubah data

- **Ganti anggota tim / urutan awal:** edit `order` di `docs/state.json`. Jaga
  `cycle`, `order`, `history`, dan `last_reshuffled` tetap konsisten.
- **Ubah pola shift (`PATTERN`):** ⚠️ pola di-hardcode di **dua tempat** —
  `reshuffle.py` dan `docs/index.html`. **Wajib ubah keduanya** agar tidak berbeda
  (lihat [§9](#9-catatan-penting-gotcha)).

> Setup awal (mengaktifkan GitHub Pages: Source = `main` / `/docs`) sudah dilakukan —
> halaman sudah live di URL di atas. Tidak perlu diulang kecuali repo dibuat ulang.

---

## 9. Catatan penting (gotcha)

- **`PATTERN` terduplikasi.** Ada di `reshuffle.py` (±baris 10–51) dan `docs/index.html`
  (`PATTERN` const). Saat ini keduanya sinkron dengan spreadsheet sumber. Jika diedit
  hanya di satu tempat, jadwal yang ditampilkan dan yang dihitung akan berbeda diam-diam.
- **`state.json` ditulis oleh bot Actions.** Edit manual boleh, tapi hati-hati menjaga
  konsistensi field-nya.
- **Bahasa user-facing = Indonesia.** Identifier kode & wiki = Inggris.
- **Tanpa dependency / build step.** Cukup Python standard library. Properti
  zero-infra ini sengaja dipertahankan.
```
