## ERD Diagram

```mermaid
erDiagram

    ADMIN {
        int admin_id PK
        string username
        string password
    }

    POI {
        int poi_id PK
        string name
        string description
        string image_url
        float latitude
        float longitude
    }

    LANGUAGE {
        int language_id PK
        string code
        string name
    }

    NARRATION_CONTENT {
        int content_id PK
        int poi_id FK
        int language_id FK
        string text_content
    }

    AUDIO {
        int audio_id PK
        int poi_id FK
        int language_id FK
        string audio_url
    }

    QR_CODE {
        int qr_id PK
        int poi_id FK
        string qr_type
        string qr_value
    }

    AUDIO_PACKAGE {
        int package_id PK
        string package_name
    }

    LOCATION_EVENT {
        int location_event_id PK
        float latitude
        float longitude
        datetime recorded_at
    }

    PLAYBACK_EVENT {
        int playback_event_id PK
        int poi_id FK
        int audio_id FK
        datetime started_at
        datetime ended_at
    }


    %% ================================
    %% POI / CONTENT
    %% ================================

    POI ||--o{ NARRATION_CONTENT : "has"

    LANGUAGE ||--o{ NARRATION_CONTENT : "used by"


    %% ================================
    %% POI / AUDIO
    %% ================================

    POI ||--o{ AUDIO : "has"

    LANGUAGE ||--o{ AUDIO : "used by"


    %% ================================
    %% QR CODE
    %% ================================

    POI ||--o{ QR_CODE : "identified by"


    %% ================================
    %% AUDIO PACKAGE
    %% ================================

    AUDIO_PACKAGE o{--o{ AUDIO : "contains"


    %% ================================
    %% LOCATION / ANALYTICS
    %% ================================

    POI ||--o{ PLAYBACK_EVENT : "appears in"

    AUDIO ||--o{ PLAYBACK_EVENT : "is played in"
