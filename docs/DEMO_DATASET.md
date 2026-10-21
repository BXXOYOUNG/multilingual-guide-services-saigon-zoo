# Classroom demo dataset

This project runs in an explicitly labeled simulation mode for classroom demonstrations. It is intended to let an instructor verify the complete visitor and admin flows; it is not a claim that the zoo approved the content, images, locations, or synthetic voices.

## Included demo content

- 11 animal POIs with localized content in Vietnamese, English, French, Simplified Chinese, Japanese, and Korean.
- 11 approximate map positions and 35 m circular geofences for testing nearest POI and auto-play. Use the map's GPS simulation button to trigger a selected point from a laptop or phone.
- 66 generated Edge TTS MP3s, one per POI and supported language, stored in SeaweedFS and registered in MongoDB as `audio_assets` with ObjectId references and SHA-256 metadata.
- Local animal photos downloaded from Wikimedia Commons, with file page, creator, and license recorded in `data/dataset/demo_image_credits.json`.
- QR flows for resolving a POI audio and downloading a selected-language offline audio package.
- Six prebuilt offline packages (vi/en/fr/zh-Hans/ja/ko), each with 11 recordings. The homepage shows one QR per language; each QR represents one package.

The app shows a localized demo banner. Map positions are approximate and the generated voices/content are simulations. Do not present them as official zoo directions or recordings.

## Seed and regenerate

Do not run seed as a normal startup or transfer step. For an existing system, restore the database and storage backups following `HUONG_DAN_CAI_DAT_VA_BAN_GIAO.md`. Regeneration can replace audio and package membership; back up first.

The content script is restricted to the development database `saigon_zoo_tcv_dataset_dev`. Dry-run first:

```powershell
.\.venv\Scripts\python.exe scripts\seed_demo_experience.py
```

Apply the 11 POIs, translations, images, and geofences, then generate/upload all 66 audio files:

```powershell
.\.venv\Scripts\python.exe scripts\seed_demo_experience.py --apply --generate-audio
```

The audio generation requires Internet connectivity and the running SeaweedFS S3 container. It is repeatable: it overwrites each deterministic demo object key and upserts the matching database records.

To download/refresh animal photos and the attribution manifest:

```powershell
.\.venv\Scripts\python.exe scripts\download_demo_images.py
```

## Run the phone demo

```powershell
.\scripts\start_demo.ps1
```

The script starts the API and Vite client, exposes the client through an HTTPS tunnel, and writes the phone URL and QR code beneath `.demo-run/`. The temporary URL expires when the tunnel stops. Bootstrap an admin account once using the instructions in `docs/DEVELOPMENT.md`.

## Data shape

`poi_id` references in localization, audio task/asset, package, geofence, analytics, and playback collections remain BSON ObjectIds. Demo status is stored explicitly as `is_demo: true`, `coordinate_status: DEMO_APPROXIMATE_NOT_VERIFIED`, and `audio_status: DEMO_TTS_READY`.
