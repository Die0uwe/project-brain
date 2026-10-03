---
id: famfinder
type: repo
bijgewerkt: 2026-10-03
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

## Belangrijke beslissingen
- 2026-10-03: de debug-build verwees naar een keystore die in `.gitignore` staat en dus ontbrak, waardoor `assembleDebug` in CI faalde. Opgelost door de standaard debug-keystore van de Android Gradle Plugin te gebruiken en de release-signing alleen actief te maken als een `STORE_PASSWORD`-secret bestaat (commit beb7209, via branch `fix/debug-apk-build` naar main).

## Openstaande punten
- `google-services.json` ontbreekt (staat niet in de repo): Firebase- en Gemini-functies werken pas na toevoegen.
- Het bouwresultaat is in CI gelukt (artifact ca. 28 MB); de APK is nog niet op een toestel getest.
- Geen README in de repo.
