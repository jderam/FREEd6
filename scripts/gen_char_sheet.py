"""Generate a FREEd6 character and write a single-page printable text character sheet.

Example calls:
    # Print a random level-1 character sheet to stdout
    uv run scripts/gen_char_sheet.py

    # Generate a named level-3 character
    uv run scripts/gen_char_sheet.py --name="Aldric" --level=3

    # Write a level-5 character sheet to a file
    uv run scripts/gen_char_sheet.py --level=5 --output=aldric.txt

    # Named level-2 character written to a file
    uv run scripts/gen_char_sheet.py --level=2 --name="Sable" --output=sable_sheet.txt
"""

import argparse
import textwrap

from free_d6.char import Character

BOX_W = 88
INNER = BOX_W - 2  # usable width between the ║ walls

# Panel columns: left content │ right drawing area
LEFT_W = 32
RIGHT_W = INNER - LEFT_W - 1  # 37


# ── Box-drawing helpers ──────────────────────────────────────────────


def box_top() -> str:
    return f"╔{'═' * INNER}╗"


def box_bottom() -> str:
    return f"╚{'═' * INNER}╝"


def box_sep() -> str:
    return f"╠{'═' * INNER}╣"


def bline(text: str = "") -> str:
    """A full-width line of content inside the box."""
    return f"║{text:<{INNER}}║"


def panel_top() -> str:
    """Double-line separator that starts the vertical divider."""
    return f"╠{'═' * LEFT_W}╤{'═' * RIGHT_W}╣"


def panel_bottom() -> str:
    """Double-line separator that ends the vertical divider."""
    return f"╠{'═' * LEFT_W}╧{'═' * RIGHT_W}╣"


def panel_sep() -> str:
    """Light separator between sections (left side only, drawing area unbroken)."""
    return f"╟{'─' * LEFT_W}┤{' ' * RIGHT_W}║"


def cline(text: str = "") -> str:
    """A content line inside the panel (left content + divider + right blank)."""
    return f"║{text:<{LEFT_W}}│{' ' * RIGHT_W}║"


def wrap_text(text: str, indent: int = 4) -> list[str]:
    """Wrap text to fit inside the box, returning a list of bline() strings."""
    pad = " " * indent
    wrapped = textwrap.fill(
        text,
        width=INNER - 1,
        initial_indent=pad,
        subsequent_indent=pad + "  ",
    )
    return [bline(ln) for ln in wrapped.split("\n")]


# ── Sheet renderer ───────────────────────────────────────────────────


def render_sheet(char: Character) -> str:
    lines: list[str] = []

    # ── Title ──
    lines.append(box_top())
    lines.append(bline("⚂ ⚄ ⚅  FREEd6  CHARACTER  ⚂ ⚄ ⚅".center(INNER)))
    lines.append(box_sep())

    # ── Vital stats (two-column, no divider) ──
    stat_left_w = 38
    name_display = char.name if char.name else "________________________"
    hp_hearts = " ♡" * char.hit_points
    lines.append(bline(f"{'  NAME: ' + name_display:<{stat_left_w}}LEVEL: {char.level}"))
    lines.append(
        bline(f"{'  BACKGROUND: ' + char.background:<{stat_left_w}}HIT POINTS:{hp_hearts}")
    )

    # ── Begin panel (5 sections + right drawing area) ──
    lines.append(panel_top())

    # Skills
    lines.append(cline("  SKILLS"))
    for skill in char.skills:
        for name in skill:
            lines.append(cline(f"    ◆ {name}"))
    lines.append(cline())

    # Extraordinary Abilities
    if char.extraordinary_abilities:
        lines.append(panel_sep())
        lines.append(cline("  EXTRAORDINARY ABILITIES"))
        for ea in char.extraordinary_abilities:
            for name in ea:
                if " (" in name:
                    base, paren = name.split(" (", 1)
                    lines.append(cline(f"    ◆ {base}"))
                    lines.append(cline(f"      ({paren}"))
                else:
                    lines.append(cline(f"    ◆ {name}"))
        lines.append(cline())

    # Weapons
    lines.append(panel_sep())
    lines.append(cline("  WEAPONS"))
    weapon_parts = char.weapon.split(", ", 1)
    lines.append(cline(f"    ◆ {weapon_parts[0]}"))
    if len(weapon_parts) > 1:
        lines.append(cline(f"      {weapon_parts[1]}"))
    lines.append(cline())

    # Equipment
    lines.append(panel_sep())
    lines.append(cline("  EQUIPMENT"))
    for item in char.equipment:
        lines.append(cline(f"    ◆ {item}"))
    lines.append(cline())

    # Money
    lines.append(panel_sep())
    lines.append(cline(f"  MONEY: {char.money} sp"))
    lines.append(cline())

    # ── End panel ──
    lines.append(panel_bottom())

    # ── Spells (full width, below panel) ──
    if char.spells:
        lines.append(bline("  SPELLS"))
        for spell in char.spells:
            for name, desc in spell.items():
                lines.extend(wrap_text(f"◆ {name}: {desc}"))
        lines.append(bline())
        lines.append(box_sep())

    # ── Notes ──
    lines.append(bline("  NOTES"))
    for _ in range(4):
        lines.append(bline())
    lines.append(bline())
    lines.append(box_bottom())

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a FREEd6 character sheet.")
    parser.add_argument("-l", "--level", type=int, default=1, help="Character level (default: 1)")
    parser.add_argument("-n", "--name", type=str, default="", help="Character name")
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output file (default: print to stdout)"
    )
    args = parser.parse_args()

    char = Character(level=args.level)
    char.name = args.name
    sheet = render_sheet(char)

    if args.output:
        with open(args.output, "w") as f:
            f.write(sheet)
        print(f"Character sheet written to {args.output}")
    else:
        print(sheet)


if __name__ == "__main__":
    main()
