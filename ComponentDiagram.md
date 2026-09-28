## Component Diagram

```mermaid
flowchart TB

    %% =====================================================
    %% VISITOR FUNCTIONS
    %% =====================================================
    subgraph VISITOR["Visitor Functions"]

        LANGUAGE["<<component>><br/>Language Preference<br/><small>UC-01</small>"]

        MAP["<<component>><br/>Map & POI View<br/><small>UC-02</small>"]

        QR_SCAN["<<component>><br/>QR Scanner<br/><small>UC-04, UC-05</small>"]

        DISCOVERY["<<component>><br/>Offline Discovery<br/><small>UC-06</small>"]
    end


    %% =====================================================
    %% COMMUNICATION BRIDGES - VISITOR
    %% =====================================================

    LANG_BRIDGE((Language<br/>Access))
    CONTENT_BRIDGE((Content<br/>Access))
    QR_BRIDGE((QR<br/>Access))
    OFFLINE_BRIDGE((Offline<br/>Access))


    LANGUAGE --> LANG_BRIDGE
    MAP --> CONTENT_BRIDGE
    QR_SCAN --> QR_BRIDGE
    QR_SCAN --> OFFLINE_BRIDGE
    DISCOVERY --> OFFLINE_BRIDGE


    %% =====================================================
    %% CORE TOUR SERVICES
    %% =====================================================
    subgraph TOUR["Tour & Narration Services"]

        POI["<<component>><br/>POI Service"]

        LOCATION["<<component>><br/>Location & Geofence Service"]

        NARRATION["<<component>><br/>Narration Service"]

        LOCALIZATION["<<component>><br/>Localization Service"]

        AUDIO["<<component>><br/>Audio Service"]
    end


    %% =====================================================
    %% INTERNAL COMMUNICATION BRIDGES
    %% =====================================================

    POI_BRIDGE((POI<br/>Access))

    NARRATION_TRIGGER((Narration<br/>Trigger))

    LANGUAGE_SERVICE((Localization<br/>Request))

    AUDIO_BRIDGE((Audio<br/>Request))


    %% Visitor -> Core
    CONTENT_BRIDGE --> POI_BRIDGE
    POI_BRIDGE --> POI

    LANG_BRIDGE --> LANGUAGE_SERVICE
    LANGUAGE_SERVICE --> LOCALIZATION

    QR_BRIDGE --> POI_BRIDGE

    OFFLINE_BRIDGE --> AUDIO_BRIDGE
    AUDIO_BRIDGE --> AUDIO


    %% Core service communication
    LOCATION --> NARRATION_TRIGGER
    NARRATION_TRIGGER --> NARRATION

    NARRATION --> POI_BRIDGE
    NARRATION --> LANGUAGE_SERVICE
    NARRATION --> AUDIO_BRIDGE


    %% =====================================================
    %% ADMIN FUNCTIONS
    %% =====================================================
    subgraph ADMIN["Administration Functions"]

        AUTH["<<component>><br/>Authentication"]

        POI_MANAGEMENT["<<component>><br/>POI Management<br/><small>UC-08</small>"]

        CONTENT_MANAGEMENT["<<component>><br/>Narration & Translation<br/>Management<br/><small>UC-09</small>"]

        ANALYTICS["<<component>><br/>Analytics<br/><small>UC-10</small>"]
    end


    %% =====================================================
    %% ADMIN BRIDGES
    %% =====================================================

    AUTH_BRIDGE((Authentication<br/>Interface))

    MANAGEMENT_BRIDGE((Management<br/>Interface))

    ANALYTICS_BRIDGE((Analytics<br/>Event))


    AUTH --> AUTH_BRIDGE

    POI_MANAGEMENT --> MANAGEMENT_BRIDGE
    CONTENT_MANAGEMENT --> MANAGEMENT_BRIDGE

    LOCATION --> ANALYTICS_BRIDGE
    POI --> ANALYTICS_BRIDGE
    AUDIO --> ANALYTICS_BRIDGE

    ANALYTICS_BRIDGE --> ANALYTICS


    %% Management -> Core
    MANAGEMENT_BRIDGE --> POI
    MANAGEMENT_BRIDGE --> LOCALIZATION
    MANAGEMENT_BRIDGE --> AUDIO


    %% =====================================================
    %% DATA / STORAGE
    %% =====================================================
    subgraph STORAGE["System Data"]

        DATA_STORE[("Application Data")]

        AUDIO_STORAGE[("Audio Storage")]
    end


    %% =====================================================
    %% DATA ACCESS BRIDGES
    %% =====================================================

    DATA_BRIDGE((Data<br/>Access))

    AUDIO_STORAGE_BRIDGE((Audio Storage<br/>Access))


    %% Core -> Data
    POI --> DATA_BRIDGE
    LOCATION --> DATA_BRIDGE
    LOCALIZATION --> DATA_BRIDGE
    AUTH --> DATA_BRIDGE
    ANALYTICS --> DATA_BRIDGE

    DATA_BRIDGE --> DATA_STORE

    AUDIO --> AUDIO_STORAGE_BRIDGE
    AUDIO_STORAGE_BRIDGE --> AUDIO_STORAGE


    %% =====================================================
    %% STYLING
    %% =====================================================

    classDef component fill:#ffffff,stroke:#333333,stroke-width:2px,color:#111111;
    classDef bridge fill:#f5f5f5,stroke:#555555,stroke-width:2px,color:#111111;
    classDef store fill:#eeeeee,stroke:#333333,stroke-width:2px,color:#111111;

    class LANGUAGE,MAP,QR_SCAN,DISCOVERY,POI,LOCATION,NARRATION,LOCALIZATION,AUDIO,AUTH,POI_MANAGEMENT,CONTENT_MANAGEMENT,ANALYTICS component;

    class LANG_BRIDGE,CONTENT_BRIDGE,QR_BRIDGE,OFFLINE_BRIDGE,POI_BRIDGE,NARRATION_TRIGGER,LANGUAGE_SERVICE,AUDIO_BRIDGE,AUTH_BRIDGE,MANAGEMENT_BRIDGE,ANALYTICS_BRIDGE,DATA_BRIDGE,AUDIO_STORAGE_BRIDGE bridge;

    class DATA_STORE,AUDIO_STORAGE store;
