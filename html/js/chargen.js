// FREEd6 character generator. Runs in the browser; also loadable from Node for tests.

(function (root) {
  const data = typeof module !== "undefined" ? require("./data.js") : FREEd6Data;

  const WEAPON_GROUPS = ["Unarmed", "Light Melee", "Heavy Melee", "Ranged"];

  function randInt(n, rng) {
    return Math.floor(rng() * n);
  }

  function choice(items, rng) {
    return items[randInt(items.length, rng)];
  }

  // k distinct items in random order (all of them if k exceeds the list length)
  function sample(items, k, rng) {
    const pool = items.slice();
    const picked = [];
    while (picked.length < k && pool.length > 0) {
      picked.push(pool.splice(randInt(pool.length, rng), 1)[0]);
    }
    return picked;
  }

  // Hit points, skill count, and extraordinary ability count for a level.
  function rollAbilities(level, rng) {
    if (level === 0) {
      return { hitPoints: 2, skCount: 1, eaCount: 0 };
    }
    const result = { hitPoints: 3, skCount: 2, eaCount: 1 };
    for (let i = 1; i < level; i++) {
      // each level-up is weighted 3:2:1 between hit points, skills, and abilities
      const roll = randInt(6, rng);
      if (roll < 3) {
        result.hitPoints += 1;
      } else if (roll < 5) {
        result.skCount += 1;
      } else {
        result.eaCount += 1;
      }
    }
    return result;
  }

  function rollWeapon(trainedWeapon, rng) {
    switch (trainedWeapon) {
      case "Light Melee":
        return choice(data.LIGHT_MELEE_WEAPONS, rng);
      case "Heavy Melee":
        return choice(data.HEAVY_MELEE_WEAPONS, rng);
      case "Ranged":
        return choice(data.RANGED_WEAPONS, rng);
      case "Unarmed":
        return "Unarmed";
      default:
        return choice(
          data.LIGHT_MELEE_WEAPONS.concat(data.HEAVY_MELEE_WEAPONS, data.RANGED_WEAPONS),
          rng
        );
    }
  }

  // Three random spells, listed in table order.
  function rollSpells(rng) {
    const picked = new Set(sample(Object.keys(data.SPELLS), 3, rng));
    return Object.keys(data.SPELLS)
      .filter((name) => picked.has(name))
      .map((name) => ({ [name]: data.SPELLS[name] }));
  }

  // Generates a random character of the given level as a plain object.
  function generateCharacter(level = 0, rng = Math.random) {
    const abilities = rollAbilities(level, rng);
    const skills = sample(data.SKILLS, abilities.skCount, rng);

    let trainedWeapon = null;
    let hasWizardry = false;
    const extraordinaryAbilities = sample(
      data.EXTRAORDINARY_ABILITIES,
      abilities.eaCount,
      rng
    ).map((ea) => {
      const name = Object.keys(ea)[0];
      if (name === "Wizardry") {
        hasWizardry = true;
      }
      if (name !== "Weapon Training") {
        return ea;
      }
      trainedWeapon = choice(WEAPON_GROUPS, rng);
      return {
        [`Weapon Training (${trainedWeapon})`]: `You make ${trainedWeapon} combat checks as skilled.`,
      };
    });

    const spells = hasWizardry ? rollSpells(rng) : [];
    const weapon = rollWeapon(trainedWeapon, rng);
    const equipment = data.BASE_EQUIPMENT.slice();
    for (const items of [
      data.CLOTHING_ITEMS,
      data.EQUIPMENT_A,
      data.EQUIPMENT_B,
      data.EQUIPMENT_C,
    ]) {
      equipment.push(choice(items, rng));
    }
    const background = choice(data.BACKGROUNDS, rng);
    const money = randInt(6, rng) + randInt(6, rng) + randInt(6, rng) + 3; // 3d6

    return {
      name: "",
      level: level,
      hit_points: abilities.hitPoints,
      sk_count: abilities.skCount,
      ea_count: abilities.eaCount,
      skills: skills,
      extraordinary_abilities: extraordinaryAbilities,
      trained_weapon: trainedWeapon,
      spells: spells,
      weapon: weapon,
      equipment: equipment,
      background: background,
      money: money,
    };
  }

  // Random name from the Zothique name lists; gender is "female", "male", or anything else for either.
  function generateName(gender = "any", rng = Math.random) {
    const names = typeof module !== "undefined" ? require("./zothique_names.js") : FREEd6Names;
    switch (String(gender).toLowerCase()) {
      case "female":
        return choice(names.FEMALE_NAMES, rng);
      case "male":
        return choice(names.MALE_NAMES, rng);
      default:
        return choice(names.FEMALE_NAMES.concat(names.MALE_NAMES), rng);
    }
  }

  const api = { generateCharacter, generateName };
  if (typeof module !== "undefined") {
    module.exports = api;
  } else {
    root.FREEd6 = api;
  }
})(typeof window !== "undefined" ? window : globalThis);
