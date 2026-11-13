// Renders a random character into chargen.html based on the `level` and `name` query parameters.

(function () {
  function setText(id, text) {
    document.getElementById(id).textContent = text;
  }

  // Fill a <ul> with one <li> per entry; entries are plain strings or [label, description] pairs.
  function setList(id, entries) {
    const list = document.getElementById(id);
    list.replaceChildren(
      ...entries.map((entry) => {
        const li = document.createElement("li");
        if (Array.isArray(entry)) {
          const label = document.createElement("b");
          label.textContent = entry[0];
          li.append(label, `: ${entry[1]}`);
        } else {
          li.textContent = entry;
        }
        return li;
      })
    );
  }

  function sortedNames(entries) {
    return entries.map((entry) => Object.keys(entry)[0]).sort();
  }

  const params = new URLSearchParams(window.location.search);

  let level = 1;
  if (params.has("level")) {
    const requested = Number(params.get("level"));
    if (Number.isInteger(requested) && requested >= 0) {
      level = requested;
    }
  }

  const pc = FREEd6.generateCharacter(level);
  if (params.get("name") === "auto") {
    pc.name = FREEd6.generateName();
  } else if (params.has("name")) {
    pc.name = params.get("name");
  }

  setText("name", pc.name);
  setText("level", pc.level);
  setText("hit-points", pc.hit_points);
  setText("background", pc.background);
  setList("skills", sortedNames(pc.skills));
  setList("extraordinary-abilities", sortedNames(pc.extraordinary_abilities));
  setList("weapon", [pc.weapon]);
  setList("equipment", pc.equipment);
  setText("money", pc.money);
  setList(
    "spells",
    pc.spells.map((spell) => Object.entries(spell)[0])
  );
  document.getElementById("spells-section").hidden = pc.spells.length === 0;
})();
