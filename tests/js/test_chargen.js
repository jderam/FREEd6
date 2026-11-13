// Tests for the browser character generator. Run with: node tests/js/test_chargen.js

const assert = require("assert");
const data = require("../../html/js/data.js");
const names = require("../../html/js/zothique_names.js");
const { generateCharacter, generateName } = require("../../html/js/chargen.js");

const keys = (entries) => entries.map((entry) => Object.keys(entry)[0]);
const allWeapons = [
  ...data.LIGHT_MELEE_WEAPONS,
  ...data.HEAVY_MELEE_WEAPONS,
  ...data.RANGED_WEAPONS,
];

// level 0 is fixed
for (let i = 0; i < 50; i++) {
  const pc = generateCharacter(0);
  assert.deepStrictEqual([pc.hit_points, pc.sk_count, pc.ea_count], [2, 1, 0]);
  assert.deepStrictEqual(pc.extraordinary_abilities, []);
  assert.deepStrictEqual(pc.spells, []);
}

const seen = { wizardry: 0, trained: new Set(), levelUps: new Set() };
for (let i = 0; i < 5000; i++) {
  const level = 1 + (i % 9);
  const pc = generateCharacter(level);

  assert.strictEqual(pc.name, "");
  assert.strictEqual(pc.level, level);
  // every level past 1 adds exactly one hit point, skill, or ability
  assert.strictEqual(pc.hit_points + pc.sk_count + pc.ea_count, 6 + level - 1);
  assert.ok(pc.hit_points >= 3 && pc.sk_count >= 2 && pc.ea_count >= 1);
  if (level > 1) {
    seen.levelUps.add(`${pc.hit_points > 3}${pc.sk_count > 2}${pc.ea_count > 1}`);
  }

  const skills = keys(pc.skills);
  assert.strictEqual(skills.length, pc.sk_count);
  assert.strictEqual(new Set(skills).size, skills.length);
  assert.ok(pc.skills.every((sk) => data.SKILLS.includes(sk)));

  const eas = keys(pc.extraordinary_abilities);
  assert.strictEqual(eas.length, pc.ea_count);
  assert.strictEqual(new Set(eas).size, eas.length);
  assert.ok(!eas.includes("Weapon Training"), "weapon group should be resolved");

  const trained = eas.find((ea) => ea.startsWith("Weapon Training"));
  if (trained) {
    assert.strictEqual(trained, `Weapon Training (${pc.trained_weapon})`);
    seen.trained.add(pc.trained_weapon);
    const expected = {
      Unarmed: ["Unarmed"],
      "Light Melee": data.LIGHT_MELEE_WEAPONS,
      "Heavy Melee": data.HEAVY_MELEE_WEAPONS,
      Ranged: data.RANGED_WEAPONS,
    }[pc.trained_weapon];
    assert.ok(expected.includes(pc.weapon));
  } else {
    assert.strictEqual(pc.trained_weapon, null);
    assert.ok(allWeapons.includes(pc.weapon));
  }

  if (eas.includes("Wizardry")) {
    seen.wizardry += 1;
    const spells = keys(pc.spells);
    assert.strictEqual(new Set(spells).size, 3);
    assert.ok(pc.spells.every((sp) => data.SPELLS[Object.keys(sp)[0]] === Object.values(sp)[0]));
  } else {
    assert.deepStrictEqual(pc.spells, []);
  }

  assert.deepStrictEqual(pc.equipment.slice(0, 5), data.BASE_EQUIPMENT);
  assert.ok(data.CLOTHING_ITEMS.includes(pc.equipment[5]));
  assert.ok(data.EQUIPMENT_A.includes(pc.equipment[6]));
  assert.ok(data.EQUIPMENT_B.includes(pc.equipment[7]));
  assert.ok(data.EQUIPMENT_C.includes(pc.equipment[8]));
  assert.strictEqual(pc.equipment.length, 9);
  assert.ok(data.BACKGROUNDS.includes(pc.background));
  assert.ok(Number.isInteger(pc.money) && pc.money >= 3 && pc.money <= 18);
}
assert.ok(seen.wizardry > 0);
assert.strictEqual(seen.trained.size, 4);
assert.strictEqual(seen.levelUps.size > 1, true);

// generating characters must not alter the shared data tables
assert.ok(keys(data.EXTRAORDINARY_ABILITIES).includes("Weapon Training"));
assert.strictEqual(data.BASE_EQUIPMENT.length, 5);

// a level high enough to exhaust the tables still works
const epic = generateCharacter(200);
assert.ok(epic.skills.length <= data.SKILLS.length);

// level-up weights are 3:2:1; rng values just under each boundary pick hp, skill, ability
assert.strictEqual(generateCharacter(2, () => 0.49).hit_points, 4);
assert.strictEqual(generateCharacter(2, () => 0.82).sk_count, 3);
assert.strictEqual(generateCharacter(2, () => 0.99).ea_count, 2);

for (let i = 0; i < 200; i++) {
  assert.ok(names.FEMALE_NAMES.includes(generateName("female")));
  assert.ok(names.MALE_NAMES.includes(generateName("Male")));
  const any = generateName();
  assert.ok(names.FEMALE_NAMES.includes(any) || names.MALE_NAMES.includes(any));
}

console.log("all chargen tests passed");
