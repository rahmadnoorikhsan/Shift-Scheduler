import json
import random
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("docs/state.json")

# Pola shift per posisi (index 0-4), per hari (0=Sen ... 6=Min), 5 minggu
# Format: PATTERN[posisi][minggu][hari]
PATTERN = [
    # Posisi 0
    [
        ["S2","S2","S2","LIBUR","S1","LIBUR","S1"],
        ["S1","S1","S1","S1","LIBUR","S2","LIBUR"],
        ["LIBUR","S1","S1","S1","S1","S1","LIBUR"],
        ["S1","LIBUR","S2","S2","S2","S2","LIBUR"],
        ["S2","S2","LIBUR","S2","S2","LIBUR","S2"],
    ],
    # Posisi 1
    [
        ["S1","S1","S1","S1","LIBUR","S2","LIBUR"],
        ["LIBUR","S1","S1","S1","S1","S1","LIBUR"],
        ["S1","LIBUR","S2","S2","S2","S2","LIBUR"],
        ["S2","S2","LIBUR","S2","S2","LIBUR","S2"],
        ["S2","S2","S2","LIBUR","S1","LIBUR","S1"],
    ],
    # Posisi 2
    [
        ["LIBUR","S1","S1","S1","S1","S1","LIBUR"],
        ["S1","LIBUR","S2","S2","S2","S2","LIBUR"],
        ["S2","S2","LIBUR","S2","S2","LIBUR","S2"],
        ["S2","S2","S2","LIBUR","S1","LIBUR","S1"],
        ["S1","S1","S1","S1","LIBUR","S2","LIBUR"],
    ],
    # Posisi 3
    [
        ["S1","LIBUR","S2","S2","S2","S2","LIBUR"],
        ["S2","S2","LIBUR","S2","S2","LIBUR","S2"],
        ["S2","S2","S2","LIBUR","S1","LIBUR","S1"],
        ["S1","S1","S1","S1","LIBUR","S2","LIBUR"],
        ["LIBUR","S1","S1","S1","S1","S1","LIBUR"],
    ],
    # Posisi 4
    [
        ["S2","S2","LIBUR","S2","S2","LIBUR","S2"],
        ["S2","S2","S2","LIBUR","S1","LIBUR","S1"],
        ["S1","S1","S1","S1","LIBUR","S2","LIBUR"],
        ["LIBUR","S1","S1","S1","S1","S1","LIBUR"],
        ["S1","LIBUR","S2","S2","S2","S2","LIBUR"],
    ],
]

def get_shift(position: int, week: int, day: int) -> str:
    return PATTERN[position][week][day]

def week5_sunday_shift(position: int) -> str:
    return get_shift(position, 4, 6)  # minggu ke-5 (idx 4), hari Minggu (idx 6)

def week1_monday_shift(position: int) -> str:
    return get_shift(position, 0, 0)  # minggu ke-1 (idx 0), hari Senin (idx 0)

WORKING_SHIFTS = {"S1", "S2"}  # shift yang dihitung "bertugas" (bukan LIBUR)

def allowed_monday_shifts(current_order: list[str]) -> dict[str, set[str]]:
    """Tentukan shift Senin Week 1 yang diizinkan untuk tiap personil.

    Constraint berbasis SEAT, bukan nama: siapa pun yang menempati seat yang masih
    bertugas di hari Minggu Week 5 tidak boleh ganti tipe shift pada Senin Week 1
    tanpa libur di antaranya. Jadi yang mengakhiri siklus dengan S1 -> Senin
    berikutnya harus {S1, LIBUR}; yang S2 -> harus {S2, LIBUR}. Seat yang LIBUR di
    Minggu W5 bebas pindah ke mana saja (tidak masuk dict).
    """
    allowed: dict[str, set[str]] = {}
    for seat, person in enumerate(current_order):
        end_shift = week5_sunday_shift(seat)
        if end_shift in WORKING_SHIFTS:
            allowed[person] = {end_shift, "LIBUR"}
    return allowed

def reshuffle_with_constraint(current_order: list[str]) -> list[str]:
    allowed = allowed_monday_shifts(current_order)

    for _ in range(10_000):
        shuffled = current_order.copy()
        random.shuffle(shuffled)

        if shuffled == current_order:
            continue

        # Setiap personil yang terkena constraint harus mendapat seat baru yang
        # shift Senin W1-nya sesuai (shift sama, atau LIBUR).
        if all(
            week1_monday_shift(shuffled.index(person)) in allowed_shifts
            for person, allowed_shifts in allowed.items()
        ):
            return shuffled

    raise RuntimeError("Tidak ditemukan urutan valid setelah 10.000 percobaan.")

def main():
    state = json.loads(STATE_FILE.read_text())

    old_order = state["order"]
    new_order = reshuffle_with_constraint(old_order)

    state["cycle"]  += 1
    state["order"]   = new_order
    state["last_reshuffled"] = datetime.now(timezone.utc).isoformat()
    state["history"].append({
        "cycle": state["cycle"],
        "order": new_order
    })

    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"✅ Reshuffle selesai — siklus {state['cycle']}")
    print(f"   Urutan baru: {' → '.join(new_order)}")

if __name__ == "__main__":
    main()
