import random

from free_d6.char import Character
from free_d6.data import (
    BACKGROUNDS,
    BASE_EQUIPMENT,
    CLOTHING_ITEMS,
    EQUIPMENT_A,
    EQUIPMENT_B,
    EQUIPMENT_C,
    LIGHT_MELEE_WEAPONS,
    HEAVY_MELEE_WEAPONS,
    RANGED_WEAPONS,
    SPELLS,
)

ALL_WEAPONS = LIGHT_MELEE_WEAPONS + HEAVY_MELEE_WEAPONS + RANGED_WEAPONS + ["Unarmed"]
ALL_EQUIPMENT = CLOTHING_ITEMS + EQUIPMENT_A + EQUIPMENT_B + EQUIPMENT_C


def test_level_0_character():
    random.seed(42)
    c = Character(level=0)
    assert c.level == 0
    assert c.hit_points == 2
    assert c.sk_count == 1
    assert c.ea_count == 0
    assert len(c.skills) == 1
    assert len(c.extraordinary_abilities) == 0


def test_level_1_character():
    random.seed(42)
    c = Character(level=1)
    assert c.level == 1
    assert c.hit_points == 3
    assert c.sk_count == 2
    assert c.ea_count == 1
    assert len(c.skills) == 2
    assert len(c.extraordinary_abilities) == 1


def test_higher_level_advancement():
    random.seed(42)
    c = Character(level=5)
    assert c.hit_points >= 3
    assert c.sk_count >= 2
    assert c.ea_count >= 1
    total = (c.hit_points - 3) + (c.sk_count - 2) + (c.ea_count - 1)
    assert total == 4  # 4 additional level-ups from levels 2-5


def test_skills_are_unique():
    random.seed(42)
    c = Character(level=5)
    skill_names = [list(s.keys())[0] for s in c.skills]
    assert len(skill_names) == len(set(skill_names))


def test_extraordinary_abilities_are_unique():
    random.seed(42)
    c = Character(level=5)
    ea_names = [list(ea.keys())[0] for ea in c.extraordinary_abilities]
    assert len(ea_names) == len(set(ea_names))


def test_weapon_is_valid():
    random.seed(42)
    for level in range(6):
        c = Character(level=level)
        assert c.weapon in ALL_WEAPONS


def test_equipment():
    random.seed(42)
    c = Character(level=1)
    assert len(c.equipment) == 9
    for item in BASE_EQUIPMENT:
        assert item in c.equipment
    random_items = [item for item in c.equipment if item not in BASE_EQUIPMENT]
    assert len(random_items) == 4
    for item in random_items:
        assert item in ALL_EQUIPMENT


def test_background_is_valid():
    random.seed(42)
    c = Character(level=1)
    assert c.background in BACKGROUNDS


def test_money_range():
    random.seed(42)
    for level in range(6):
        c = Character(level=level)
        assert 3 <= c.money <= 18


def test_as_dict():
    random.seed(42)
    c = Character(level=1)
    d = c.as_dict()
    assert isinstance(d, dict)
    expected_keys = {
        "name",
        "level",
        "hit_points",
        "sk_count",
        "ea_count",
        "skills",
        "extraordinary_abilities",
        "trained_weapon",
        "spells",
        "weapon",
        "equipment",
        "background",
        "money",
    }
    assert expected_keys.issubset(d.keys())


def test_weapon_training():
    random.seed(0)
    # Generate characters until we find one with Weapon Training
    found = False
    for _ in range(500):
        c = Character(level=5)
        if c.has_weapon_training:
            found = True
            assert c.trained_weapon in ["Unarmed", "Light Melee", "Heavy Melee", "Ranged"]
            if c.trained_weapon == "Light Melee":
                assert c.weapon in LIGHT_MELEE_WEAPONS
            elif c.trained_weapon == "Heavy Melee":
                assert c.weapon in HEAVY_MELEE_WEAPONS
            elif c.trained_weapon == "Ranged":
                assert c.weapon in RANGED_WEAPONS
            elif c.trained_weapon == "Unarmed":
                assert c.weapon == "Unarmed"
            break
    assert found, "No character with Weapon Training generated"


def test_wizardry_spells():
    random.seed(0)
    # Generate characters until we find one with Wizardry
    for _ in range(500):
        c = Character(level=3)
        if c.has_wizardry:
            assert len(c.spells) == 3
            for spell in c.spells:
                assert isinstance(spell, dict)
                spell_name = next(iter(spell))
                assert spell_name in SPELLS
            return
    raise AssertionError("No character with Wizardry generated")


def test_no_wizardry_no_spells():
    random.seed(42)
    c = Character(level=0)
    assert not c.has_wizardry
    assert c.spells == []
