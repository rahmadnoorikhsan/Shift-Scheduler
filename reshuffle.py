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
        ["S2","S1","S2","LIBUR","S1","LIBUR","S1"],
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

def reshuffle_with_constraint(current_order: list[str]) -> list[str]:
    djaloe_old_pos = current_order.index("Djaloe")
    aji_old_pos    = current_order.index("Aji")

    djaloe_end = week5_sunday_shift(djaloe_old_pos)
    aji_end    = week5_sunday_shift(aji_old_pos)

    # Constraint: jika akhir S2/LIBUR → awal berikutnya S2/LIBUR
    #             jika akhir S1/LIBUR → awal berikutnya S1/LIBUR
    allowed_djaloe = {"S2", "LIBUR"} if djaloe_end in {"S2", "LIBUR"} else {"S1", "LIBUR"}
    allowed_aji    = {"S1", "LIBUR"} if aji_end    in {"S1", "LIBUR"} else {"S2", "LIBUR"}

    for _ in range(10_000):
        shuffled = current_order.copy()
        random.shuffle(shuffled)

        if shuffled == current_order:
            continue

        new_djaloe_pos = shuffled.index("Djaloe")
        new_aji_pos    = shuffled.index("Aji")

        djaloe_new_mon = week1_monday_shift(new_djaloe_pos)
        aji_new_mon    = week1_monday_shift(new_aji_pos)

        if djaloe_new_mon in allowed_djaloe and aji_new_mon in allowed_aji:
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
