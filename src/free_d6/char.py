import random

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


class Character:
    """A randomly generated FREEd6 character."""

    def __init__(self, level: int = 0) -> None:
        self.name: str = ""
        self.level: int = level
        self.hit_points, self.sk_count, self.ea_count = self._roll_abilities()
        self.skills: list[dict[str, str]] = self._roll_skills()
        self.extraordinary_abilities: list[dict[str, str]] = self._roll_extraordinary_abilities()
        self.trained_weapon: str | None = self._resolve_weapon_training()
        self.spells: list[dict[str, str]] = self._roll_spells()
        self.weapon: str = self._roll_weapon()
        self.equipment: list[str] = self._roll_equipment()
        self.background: str = self._roll_background()
        self.money: int = self._roll_money()

    @property
    def has_wizardry(self) -> bool:
        ea_keys = [next(iter(ea)) for ea in self.extraordinary_abilities]
        return "Wizardry" in ea_keys

    @property
    def has_weapon_training(self) -> bool:
        ea_keys = [next(iter(ea)) for ea in self.extraordinary_abilities]
        return any(k.startswith("Weapon Training") for k in ea_keys)

    def _roll_abilities(self) -> tuple[int, int, int]:
        """Calculate number of hit points, skills, and extraordinary abilities based on level."""
        if self.level == 0:
            return 2, 1, 0

        # level 1
        hit_points = 3
        sk_count = 2
        ea_count = 1

        # levels 2+
        level_ups = ["hp", "sk", "ea"]
        for _ in range(self.level - 1):
            level_up = random.choices(level_ups, weights=[3, 2, 1])[0]
            if level_up == "hp":
                hit_points += 1
            elif level_up == "sk":
                sk_count += 1
            elif level_up == "ea":
                ea_count += 1
        return hit_points, sk_count, ea_count

    def _roll_skills(self) -> list[dict[str, str]]:
        return random.sample(SKILLS, k=self.sk_count)

    def _roll_extraordinary_abilities(self) -> list[dict[str, str]]:
        # shallow copy each dict to avoid mutating global data
        return [dict(ea) for ea in random.sample(EXTRAORDINARY_ABILITIES, k=self.ea_count)]

    def _resolve_weapon_training(self) -> str | None:
        """If character has Weapon Training, pick a weapon group and update the EA entry."""
        for ea in self.extraordinary_abilities:
            if next(iter(ea)) == "Weapon Training":
                trained = random.choice(["Unarmed", "Light Melee", "Heavy Melee", "Ranged"])
                ea.pop("Weapon Training")
                ea[f"Weapon Training ({trained})"] = f"You make {trained} combat checks as skilled."
                return trained
        return None

    def _roll_weapon(self) -> str:
        if self.trained_weapon == "Light Melee":
            return random.choice(LIGHT_MELEE_WEAPONS)
        elif self.trained_weapon == "Heavy Melee":
            return random.choice(HEAVY_MELEE_WEAPONS)
        elif self.trained_weapon == "Ranged":
            return random.choice(RANGED_WEAPONS)
        elif self.trained_weapon == "Unarmed":
            return "Unarmed"
        return random.choice(LIGHT_MELEE_WEAPONS + HEAVY_MELEE_WEAPONS + RANGED_WEAPONS)

    def _roll_equipment(self) -> list[str]:
        """Base equipment plus one item from each list."""
        equipment = list(BASE_EQUIPMENT)
        for items in [CLOTHING_ITEMS, EQUIPMENT_A, EQUIPMENT_B, EQUIPMENT_C]:
            equipment.append(random.choice(items))
        return equipment

    def _roll_background(self) -> str:
        return random.choice(BACKGROUNDS)

    def _roll_spells(self) -> list[dict[str, str]]:
        """Roll on the Knave spells table if character has Wizardry."""
        if not self.has_wizardry:
            return []
        spell_keys = random.sample(list(SPELLS.keys()), k=3)
        return [{k: v} for k, v in SPELLS.items() if k in spell_keys]

    def _roll_money(self) -> int:
        """Roll 3d6 for starting money."""
        return sum(random.randint(1, 6) for _ in range(3))

    def as_dict(self) -> dict:
        return self.__dict__


if __name__ == "__main__":
    from pprint import pprint

    level = random.randint(0, 9)
    print(f"{level = }")
    character = Character(level=level)
    pprint(character.as_dict())
