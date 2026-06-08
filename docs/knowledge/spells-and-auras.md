<!-- ============================================================
     Project Brain — DieOuwe Ecosysteem Kennisbank
     © 2026 DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     Licentie: CC BY-SA 4.0 — Vrij te delen met bronvermelding
     ============================================================ -->

# Spells & Auras — Geverifieerde Spell IDs
> Build: 12.0.5.67314 (Midnight) · Beheerder: data-grinder · Updated: 2026-06-08

---

## Correcte API (Midnight 12.0.5)

```lua
-- GEBRUIK DIT:
local spellInfo = C_Spell.GetSpellInfo(spellID)
if spellInfo then
    local name    = spellInfo.name
    local iconID  = spellInfo.iconID
    local castTime = spellInfo.castTime
end

-- Aura data ophalen
local auraData = C_UnitAuras.GetAuraDataByIndex(unit, index, filter)
-- filter: "HELPFUL" (buffs) | "HARMFUL" (debuffs)

-- NOOIT DIT (deprecated):
-- GetSpellInfo(spellID)
-- UnitAura(unit, i)
```

---

## Nuttige Spell IDs (Midnight)

| Naam | Spell ID | Type | Gebruik | Status |
|---|---|---|---|---|
| (community aanvulling gewenst) | ? | Buff/Debuff | — | UNVERIFIED |

> Weet jij een spell ID? Zie [contributing/templates/new-id.md](../../contributing/templates/new-id.md)

---

## Aura Events

| Event | Gebruik |
|---|---|
| `UNIT_AURA` | Buffer/debuff wijziging op unit |
| `COMBAT_LOG_EVENT_UNFILTERED` | Spell casts in combat log |

---

## Combat Log Filtering

```lua
local function OnCombatEvent(_, event, _, sourceGUID, _, _, _, destGUID, _, _, _, spellID, spellName)
    if event == "SPELL_CAST_SUCCESS" then
        -- verwerk
    end
end
local f = CreateFrame("Frame")
f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
f:SetScript("OnEvent", function(self, event)
    OnCombatEvent(CombatLogGetCurrentEventInfo())
end)
```

<!-- ============================================================
     File    : docs/knowledge/spells-and-auras.md
     Version : 1.0.0  Created: 2026-06-08  Updated: 2026-06-08
     Status  : New
     DieOuwe · www.dieouwe.nl · discord.gg/y8Pu5qsEbQ
     ============================================================ -->
