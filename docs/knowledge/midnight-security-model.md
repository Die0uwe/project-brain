# Midnight 12.0.5 Security Model — Addon Compliance
*Bron: "Addon-ontwikkeling voor WoW Midnight 12.0.5" analyse · verwerkt 2026-06-12*
*Door: data-grinder + general-researcher · voor: alle WoW skills*

## Kernmodel
Midnight = secure-aware UI engineering. Addons mogen: layout, skinning,
presentatie van al-zichtbare info, niet-combat utilities, secure templates.
Addons mogen NIET: combat-beslislogica (rotation/cooldown solving/aura
decisioning), protected frames in combat muteren, forbidden widgets aansturen.

## Secret Values (NIEUW in 12.x)
- Combat-data (cooldowns, buffs, debuffs) komt deels als "secret value" terug
  op tainted paths — weergeven mag vaak, er logica op bouwen NIET.
- Diagnose-API's: `issecretvalue(v)`, `scrubsecretvalues(...)`,
  `issecurevariable`, `C_RestrictedActions.GetAddOnRestrictionState`,
  `C_RestrictedActions.IsAddOnRestrictionActive`
- API-docs metadata: `SecretArguments = "AllowedWhenUntainted"` per functie.

## Harde limieten
- macrotext op SecureActionButtonTemplate: MAX 255 tekens (sinds 11.0.2)
- Niet-bijgewerkte addons (oude TOC) mogen NIET meer laden in Midnight
- Forbidden widgets: zelfs /click en secure clicks werken er niet op
- Combat lockdown: PLAYER_REGEN_DISABLED vuurt VÓÓR de lock,
  PLAYER_REGEN_ENABLED ná de vrijgave

## Best practices (voor WowTracker van toepassing)
- CreateFramePool / CreateFramePoolCollection voor dynamische widgets
  (roster cards, currency tiles, badges) — Blizzard's eigen patroon
- PixelUtil.SetPoint/SetWidth voor pixelstrakke layout (optioneel)
- Mixins (CreateFromMixins/Mixin) + XML virtual templates voor hergebruik
- Eén namespace-table, alles local, init op ADDON_LOADED (SavedVariables)
  en herpositionering op PLAYER_ENTERING_WORLD
- Broncode raadplegen: `/run ExportInterfaceFiles("code")` of
  github.com/Gethe/wow-ui-source (live mirror)

## Status WowTracker t.o.v. dit model: ✅ COMPLIANT
- Geen combat-beslislogica · geen protected mutaties · pooling toegepast
  (profPool v3.1.6, LOG_LINES pool) · InCombatLockdown guards aanwezig
- Aandachtspunt Fase 4: pool-refactor roster cards + currency tiles naar
  CreateFramePool, secret-aware checks waar combat-data getoond wordt.
