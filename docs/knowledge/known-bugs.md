# Known Bugs & Workarounds
> Midnight 12.0.5 · Laatste update: 2026-06-14

---

## Actieve Bugs

### BUG-001 — OptionsSliderTemplate Stille Crash
**Status**: PERMANENT (template verwijderd)
**Symptoom**: Volledig .lua bestand laadt niet, geen error in console
**Oorzaak**: `OptionsSliderTemplate` bestaat niet meer in Midnight
**Fix**: Custom slider frame bouwen zonder inheritance

### BUG-002 — FRIZQT__.TTF Missing
**Status**: PERMANENT
**Symptoom**: Font laadt niet, tekst onzichtbaar of fallback font
**Oorzaak**: Font verwijderd uit game client
**Fix**: `Fonts\2002.ttf` gebruiken

### BUG-003 — UIDropDownMenu Removed
**Status**: PERMANENT
**Symptoom**: Lua error bij aanroep
**Oorzaak**: Volledig verwijderd in Dragonflight, weg in Midnight
**Fix**: `MenuUtil.CreateContextMenu()`

### BUG-004 — Workflow Push Silent Fail
**Status**: KNOWN (GitHub PAT issue)
**Symptoom**: Push naar `.github/workflows/` werkt niet zonder `workflow` scope
**Oorzaak**: PAT heeft alleen `repo` scope, mist `workflow` scope
**Fix**: Workflows handmatig aanmaken via GitHub UI, of PAT opnieuw genereren met `workflow` scope

### BUG-005 — Skill Upload Name Mismatch
**Status**: KNOWN (Claude behavior)
**Symptoom**: Claude behandelt skill upload als nieuw skill i.p.v. update
**Oorzaak**: Lokale folder naam ≠ `name` field in YAML frontmatter
**Fix**: Folder naam en frontmatter `name` exact gelijk houden

### BUG-006 — GitHub Pages Subdir Fail
**Status**: KNOWN
**Symptoom**: GitHub Pages activeert niet op custom subdir
**Oorzaak**: Alleen `/` of `/docs` zijn geldige source paths
**Fix**: Content plaatsen in repo root of `/docs` map

---

## Opgeloste Bugs (archief)

| Bug | Datum opgelost | Oplossing |
|---|---|---|
| Kompas wijst verkeerde richting | 2026-05 | math.atan2(dx, -dy) formule geverifieerd |
| Prey detectie false positives | 2026-05 | String match vervangen door questID range check |
| Currency nil crash | 2026-04 | GetCurrencyInfo → C_CurrencyInfo.GetCurrencyInfo |

---

*Beheerd door data-grinder · VERIFIED*
