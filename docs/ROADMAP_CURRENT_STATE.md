# Current demo implementation state

Updated 2026-10-21 after the user clarified the target is a complete classroom demo with simulated content.

## Implemented demo flows

- Six-language interface and POI text: `vi`, `en`, `fr`, `zh-Hans`, `ja`, `ko`.
- 11 active simulated POIs, with localized drafts in every language and approximate map pins/geofence circles.
- A credited, locally stored animal image for each POI; attribution/license metadata is in `data/dataset/demo_image_credits.json`.
- 66 generated Edge TTS MP3 files, registered in `audio_assets` and stored in SeaweedFS, plus matching completed demo audio tasks.
- Tap a map point to view its image and play audio. Enable simulated auto-play and use “simulate GPS arrival” to exercise geofence playback from a desktop or phone.
- QR camera scan for POI narration and offline audio packages; an 11-code printable sheet is generated under `.demo-run/poi-demo-qr-sheet.html`.
- Six checksum-verified offline packages, one per language, with 11 recordings each; homepage QR cards link to each package.
- Admin login, POI/localization editing, QR generation, audio-package generation, and analytics screens.

The visitor UI displays a demo banner. Locations, written narratives, and synthetic voices are simulated classroom content and should not be presented as official zoo information or recordings.

## Demo database snapshot

Database: `saigon_zoo_tcv_dataset_dev`.

| Collection | Demo records |
|---|---:|
| `poi` | 11 active |
| `poi_localizations` | 66 |
| `geofence_zones` | 11 active simulated circles |
| `audio_tasks` | 66 completed TTS tasks |
| `audio_assets` | 66 generated recordings |
| `audio_packages` | 6 language packages, 11 recordings each |

Foreign-key-style references in MongoDB remain BSON ObjectIds. APIs serialize these as `id` hex strings.

## Repeatable setup

See [`DEMO_DATASET.md`](DEMO_DATASET.md) for the development-DB-only seed and audio-generation commands. Start the phone demo with `scripts/start_demo.ps1`; its current URL and launcher QR are stored under `.demo-run/`.

## Remaining manual demo checks

- Open the current HTTPS URL on iOS/Android and grant camera permission; the launcher URL changes whenever the tunnel is restarted.
- Print the POI QR sheet or show it on another screen, open the app’s Explore scanner, and scan the codes.
- To show automatic playback, open Map, enable simulated auto-play, select a marker, and tap the GPS simulation button for that POI.
- Sign into `/admin` with the existing demo admin account. If an account needs to be recreated, follow `docs/DEVELOPMENT.md`.

## Audit and cleanup

Read [CURRENT_ARCHITECTURE.md](CURRENT_ARCHITECTURE.md) for current diagrams, [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md) for PRD gaps, and [CLEANUP_REVIEW.md](CLEANUP_REVIEW.md) for archived files. This list of demo flows does not certify every branch of the original PRD. Runtime translation/TTS fallback, PMTiles, complete editorial workflow and physical-device camera/GPS acceptance remain gaps.
