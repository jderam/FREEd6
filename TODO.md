# TODO: code vs. rules disagreements

Found 2026-11-13 by comparing the character generator against `rules/book1/02_character_creation.md`
and `rules/book1/04_magic.md`. The rules docs are the source of truth, so the default fix is to change the code to match them. The generator's
logic is in `html/js/chargen.js` and its data tables are in `html/js/data.js`.

## Real disagreements

- [ ] **Level 0 gets too much.** The rules give a level 0 character one wearable item and three
  misc items, with no base equipment pack, no weapon and "no money". The code gives every level
  the base pack, a weapon and 3d6 sp.
- [ ] **Extraordinary abilities differ by one.** The rules list Backstab and the code doesn't. The
  code has Read Magic, which the rules' ability list omits (though the Magic chapter describes it).
- [ ] **Berserks Mode says different things.** In the rules, attacks against you have advantage.
  In the code, your own attacks have disadvantage.
- [ ] **The spell list is a different list.** The Magic chapter has a 36-spell d66 table. The code
  picks from 103 spells, 68 of which aren't in that table. Appendix C's d666 list is a third,
  unrelated set of 216 (only 2 names overlap with the code). For the 35 shared spells the
  descriptions match apart from formatting; the 36th is only a spelling difference
  ("X-Ray Vision" in the rules, "X Ray Vision" in the code).
- [ ] **Weapon odds differ.** The rules roll a d6 for the group, then a d6 within it, with six
  entries per group. The code splits combined entries ("Dagger/Stiletto",
  "Glaive/Halberd/Polearm", "Double-bladed Scimitar or Bat'leth") into separate weapons and picks
  uniformly from all 22, which makes heavy melee 9 in 22 instead of 1 in 3.
- [ ] **Abilities can't repeat.** The rules say Wizardry (and Beastmaster) can be taken more than
  once. The code never picks the same ability twice, so a character never has more than three
  spells.

## Smaller gaps

- [ ] **Healing:** the rules add "limited to once per day per character"; the code's text leaves
  it out.
- [ ] **Muscle:** the rules add "(Non-combat)"; the code's text doesn't.
- [ ] **Read Magic scrolls:** the description promises two random scrolls, but the generator gives
  none. The rules' scroll table is still marked under construction.
- [ ] **Unarmed training:** a character trained in Unarmed gets "Unarmed" as their weapon, where
  the rules say to roll or select a starting weapon.
- [ ] **Backgrounds:** the code rolls one from an 18-entry list. The rules have no background
  table and only mention background as optional flavour.
- [ ] **Level cap:** the rules' advancement chart stops at level 9; the code accepts any level.

## Typos in the rules themselves

- [ ] In `02_character_creation.md`, the second extraordinary ability group is headed "(3-6)"
  where it should be "(4-6)".
- [ ] The first extraordinary ability group has an empty item 7.

## What already matches

Hit points, skills and abilities at levels 0 and 1, the 3:2:1 level-up roll, the twelve skills, all
four equipment tables, and 3d6 sp at level 1.
