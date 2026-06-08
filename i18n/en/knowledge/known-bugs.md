> 🌐 Translation of [`docs/knowledge/known-bugs.md`](../../../docs/knowledge/known-bugs.md)
> Language: English · Translated by: DieOuwe team · Date: 2026-06-08
> ⚠️ When in doubt, always check the [original document](../../../docs/knowledge/known-bugs.md).

# Known Bugs & Workarounds
> Build target: 12.0.5.67314 (Midnight) · Maintainer: data-grinder

---

## Critical Crashes (fix immediately)

| Bug | Symptom | Fix | Version |
|---|---|---|---|
| `OptionsSliderTemplate` | Silent crash, blocks entire file | Use `MinimalSliderWithSteppers` | 12.0.x |
| `Fonts\FRIZQT__.TTF` | Font not found → addon won't load | Use `Fonts\2002.ttf` | 12.0.x |
| `UIDropDownMenu_*` / `EasyMenu` | Deprecated, taint issues | `MenuUtil.CreateContextMenu()` | 11.0+ |
| `getglobal("name")` | Deprecated, returns nil | `_G["name"]` | 11.0+ |

---

## Deprecated API Calls

| Old call | Status | Replacement |
|---|---|---|
| `GetCurrencyInfo(id)` | DEPRECATED | `C_CurrencyInfo.GetCurrencyInfo(id)` |
| `GetSpellInfo(id)` | DEPRECATED | `C_Spell.GetSpellInfo(id)` |
| `GetItemInfo(id)` | DEPRECATED | `C_Item.GetItemInfo(id)` |
| `UnitAura(unit, i)` | DEPRECATED | `C_UnitAuras.GetAuraDataByIndex(unit, i, filter)` |
| `OnUpdate` polling | AVOID | `C_Timer.NewTicker(interval, fn)` |

---

## Taint Issues

| Situation | Cause | Fix |
|---|---|---|
| Frame drag in combat | `InCombatLockdown()` not checked | Always guard at start of drag/move |
| SecureActionButton | Addon code touching secure frames | No addon code may touch secure frames |

---

## Frame / UI Bugs

| Bug | Symptom | Fix |
|---|---|---|
| Frame off-screen | Disappears on resolution change | `frame:SetClampedToScreen(true)` ALWAYS |
| Compass needle reversed | Arrow TGA points down | TGA must point UP (North) |
| 50fps animation stutters | Timer too fast / too slow | `C_Timer.NewTicker(0.02, fn)` = exact 50fps |

---

## CurseBot (Python)

| Bug | Symptom | Fix |
|---|---|---|
| `tasks.loop` stops on error | Bot goes offline silently | Add `@loop.error` handler |
| CF API rate limit | 429 responses, bot crashes | Implement exponential backoff |
| Discord token expired | Bot won't start | Renew token via Discord Developer Portal |

---

## WordPress (Slayer Alliance)

| Bug | Symptom | Fix |
|---|---|---|
| Nonce verification fails | AJAX calls blocked | Implement `wp_verify_nonce()` correctly |
| SQL injection risk | Raw `$_POST` in queries | Always use `$wpdb->prepare()` |
| Blizzard OAuth expired | API calls fail | Implement token refresh flow |

---

## Reliability legend
- **VERIFIED** — Multiple sources, self-tested or officially documented
- **PROBABLE** — One reliable source
- **UNVERIFIED** — Not tested, use with caution
