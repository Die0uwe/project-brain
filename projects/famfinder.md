---
id: famfinder
type: repo
bijgewerkt: 2026-10-13
bron_repo: Die0uwe/famfinder
---
# famfinder (app SpotFam)

## Doel
Android-app "SpotFam": familie en vrienden delen hun locatie met privacy, veilige zones, chat, SOS-noodknop en ouderlijk toezicht (bron: `metadata.json` in de repo). Repo is **privé**.

## Stack
- Kotlin, Jetpack Compose (Material 3), Room (lokale database), Firebase (BoM, `firebase-ai` voor Gemini, App Check), compileSdk 36, minSdk 24, targetSdk 36.
- Opzet afkomstig uit Google AI Studio (`metadata.json`, `.env.example` met `GEMINI_API_KEY`-plaatshouder; echte sleutel staat niet in de repo).
- 19 Kotlin-bestanden: schermen voor kaart, familie, chat en veiligheid (`ui/screens/`), `MainViewModel`, `FamilyRepository`, Room-DAO's en `LocationHelper`.

## Versie en status
- versionName 1.0 (versionCode 1), pakketnaam `com.aistudio.famguard.qv7x2k`. Status: in ontwikkeling, nog geen release.
- Laatste commit op main (2026-10-03): debug-build gerepareerd, zie hieronder.

## Build, test, deploy
- CI: `.github/workflows/build-apk.yml` bouwt bij elke push `./gradlew assembleDebug` (JDK 21) en uploadt het artifact **SpotFam-Debug-APK** (30 dagen bewaard).
- Lokale bouw vereist Android SDK en toegang tot Google/Maven; in de cloud-sandbox van Claude niet mogelijk, dus bouwen gaat via GitHub Actions.
- Installeren op een telefoon: artifact downloaden, "onbekende bronnen" toestaan, Play Protect-waarschuwing bij debug-APK accepteren. Een eerdere installatie met een andere debug-sleutel eerst verwijderen.

## Plan (advies 2026-10-13, gratis route)
- Backend op de eigen server (Docker + Cloudflare Tunnel) voor accounts, familiegroep, live locatie en chat; Firebase Cloud Messaging alleen voor push/SOS (gratis).
- Echte kaart met OpenStreetMap (osmdroid of MapLibre), geen API-sleutel nodig.
- Achtergrondlocatie via een foreground service; dit is het lastigste deel (Android-beperkingen, Play-beleid).
- Videobellen later (Jitsi-link). Verspreiden: APK zelf delen is gratis; Play Store kost eenmalig $25 en keurt achtergrondlocatie streng.
- Locatie van kinderen is AVG-gevoelig: data thuis houden.
- Eerste versie (MVP): login, familie aanmaken, live locatie op een echte kaart, chat, SOS-push. Start gepland 2026-10-14.

## Belangrijke beslissingen
- 2026-10-03: de debug-build verwees naar een keystore die in `.gitignore` staat en dus ontbrak, waardoor `assembleDebug` in CI faalde. Opgelost door de standaard debug-keystore van de Android Gradle Plugin te gebruiken en de release-signing alleen actief te maken als een `STORE_PASSWORD`-secret bestaat (commit beb7209, via branch `fix/debug-apk-build` naar main).

## Openstaande punten
- `google-services.json` ontbreekt (staat niet in de repo): Firebase- en Gemini-functies werken pas na toevoegen.
- De debug-APK is door Ouwe op een telefoon getest (2026-10-13); hij werkt als demo.
- **Geen backend** (VERIFIED, analyse van de APK 2026-10-13): alle gegevens staan lokaal in Room met nepdata (bijv. testnummers); Firebase-bibliotheken zitten erin maar de app-code roept ze niet aan. Twee telefoons zien elkaar dus niet. Videobellen is een demo (vaste `videoplayback.mp4`). De uitnodigingslink `https://spotfam.app/join/...` bestaat alleen in de app.
- Geen README in de repo.
