## Component Diagram

```mermaid
flowchart LR

    %% =========================================================
    %% CLIENT LAYER
    %% =========================================================
    subgraph CLIENT["Client Layer"]

        VISITOR["Visitor App"]

        ADMIN["Admin CMS"]

        LANG["Language Preference"]
        GPS["GPS / Location"]
        QR["QR Scanner"]
        OFFLINE["Offline Content Manager"]
        LOCAL["Local Storage"]

        VISITOR --> LANG
        VISITOR --> GPS
        VISITOR --> QR
        VISITOR --> OFFLINE

        LANG --> LOCAL
        OFFLINE --> LOCAL
    end


    %% =========================================================
    %% BACKEND LAYER
    %% =========================================================
    subgraph BACKEND["Backend Services"]

        API["Backend API / Router"]

        AUTH["Auth Service"]

        POI["POI Service"]

        QR_SERVICE["QR Service"]

        LOCATION["Location & Geofence Service"]

        NARRATION["Narration Service"]

        LOCALIZATION["Localization Service"]

        AUDIO["Audio Service"]

        ANALYTICS["Analytics Service"]

        %% Client -> Backend
        VISITOR --> API
        ADMIN --> API

        %% API -> Services
        API --> AUTH
        API --> POI
        API --> QR_SERVICE
        API --> LOCATION
        API --> NARRATION
        API --> LOCALIZATION
        API --> AUDIO
        API --> ANALYTICS

        %% Service-to-Service communication
        LOCATION -->|"POI entered"| NARRATION

        NARRATION -->|"Get POI"| POI
        NARRATION -->|"Get localized content"| LOCALIZATION
        NARRATION -->|"Get / generate audio"| AUDIO

        QR_SERVICE -->|"Resolve POI"| POI
        QR_SERVICE -->|"Resolve audio package"| AUDIO

        LOCATION -->|"Location events"| ANALYTICS
        AUDIO -->|"Playback events"| ANALYTICS
        POI -->|"POI data"| ANALYTICS
    end


    %% =========================================================
    %% DATA & EXTERNAL SERVICES
    %% =========================================================
    subgraph DATA["Data & External Services"]

        DB[("Database")]

        STORAGE[("Audio / File Storage")]

        TTS["TTS Provider"]
    end


    %% Service -> Data
    AUTH --> DB
    POI --> DB
    LOCALIZATION --> DB
    AUDIO --> DB
    ANALYTICS --> DB
    QR_SERVICE --> DB
    LOCATION --> DB

    AUDIO --> STORAGE
    AUDIO -->|"Generate speech"| TTS

    %% Offline download
    OFFLINE -->|"Download offline package"| API
