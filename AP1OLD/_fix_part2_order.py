# -*- coding: utf-8 -*-
"""Fix block order in _gen_part2_blocks.py: C → D → E."""
from pathlib import Path

path = Path(__file__).parent / "_gen_part2_blocks.py"
text = path.read_text(encoding="utf-8")

e1 = "    # ===================== BLOCK E.1 ====================="
d1 = "    # ===================== BLOCK D.1 ====================="
e_theory = "    # ===================== STAGE E THEORY ====================="

i_e1 = text.index(e1)
i_d1 = text.index(d1)
i_e_theory = text.index(e_theory)

prefix = text[:i_e1]
e_blocks = text[i_e1:i_d1]
d_blocks = text[i_d1:i_e_theory]
e_theory_tail = text[i_e_theory:]

# E.8 footer: unified doc, not part 3
e_blocks = e_blocks.replace(
    "**Этап E выполнен.** Часть 2 закончена — переходи к **части 3** (этапы F и G).",
    "**Этап E выполнен.** Backend T04 полный — переходи к **этапу F** (curl-сценарии).",
).replace(
    "Конец части 2. Открой `_t04_08_v2_part3.md` когда будет готова.",
    "Дальше — **этап F** в этом же файле.",
)

fixed = prefix + d_blocks + e_theory_tail + e_blocks
path.write_text(fixed, encoding="utf-8")
print("Fixed block order in _gen_part2_blocks.py")
