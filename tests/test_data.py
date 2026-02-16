from free_d6.data import (
    SKILLS,
    EXTRAORDINARY_ABILITIES,
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


def test_skills_structure():
    assert len(SKILLS) == 12
    for skill in SKILLS:
        assert isinstance(skill, dict)
        assert len(skill) == 1
        for name, desc in skill.items():
            assert isinstance(name, str)
            assert isinstance(desc, str)


def test_extraordinary_abilities_structure():
    assert len(EXTRAORDINARY_ABILITIES) == 12
    for ea in EXTRAORDINARY_ABILITIES:
        assert isinstance(ea, dict)
        assert len(ea) == 1
        for name, desc in ea.items():
            assert isinstance(name, str)
            assert isinstance(desc, str)


def test_backgrounds():
    assert len(BACKGROUNDS) == 18
    for bg in BACKGROUNDS:
        assert isinstance(bg, str)


def test_base_equipment():
    assert len(BASE_EQUIPMENT) == 5
    for item in BASE_EQUIPMENT:
        assert isinstance(item, str)


def test_equipment_lists():
    for items in [CLOTHING_ITEMS, EQUIPMENT_A, EQUIPMENT_B, EQUIPMENT_C]:
        assert len(items) == 6
        for item in items:
            assert isinstance(item, str)


def test_weapon_lists():
    assert len(LIGHT_MELEE_WEAPONS) == 7
    assert len(HEAVY_MELEE_WEAPONS) == 9
    assert len(RANGED_WEAPONS) == 6
    for weapon_list in [LIGHT_MELEE_WEAPONS, HEAVY_MELEE_WEAPONS, RANGED_WEAPONS]:
        for weapon in weapon_list:
            assert isinstance(weapon, str)


def test_spells():
    assert len(SPELLS) == 103
    for name, desc in SPELLS.items():
        assert isinstance(name, str)
        assert isinstance(desc, str)
