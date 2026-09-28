## Deployment Diagram

```mermaid
flowchart TB

    %% =========================================================
    %% VISITOR DEVICE
    %% =========================================================

    subgraph VISITOR_NODE["<<device>> Visitor Mobile Device"]
        direction TB

        VISITOR_APP["<<component>><br/>Visitor App"]

        VISITOR_HARDWARE["GPS<br/>Camera / QR Scanner<br/>Audio Player"]

        VISITOR_STORAGE[("Local Storage")]

        VISITOR_APP --- VISITOR_HARDWARE
        VISITOR_APP --- VISITOR_STORAGE
    end


    %% =========================================================
    %% ADMIN DEVICE
    %% =========================================================

    subgraph ADMIN_NODE["<<device>> Admin Workstation"]
        direction TB

        ADMIN_CMS["<<component>><br/>Admin CMS"]
    end


    %% =========================================================
    %% APPLICATION SERVER
    %% =========================================================

    subgraph APP_NODE["<<node>> Application Server"]
        direction TB

        %% -------------------------
        %% Main Components
        %% -------------------------

        subgraph CORE_SERVICES["Core Services"]
            direction LR

            POI["<<component>><br/>POI Service"]

            LOCATION["<<component>><br/>Location &<br/>Geofence Service"]

            QR["<<component>><br/>QR Service"]

            AUTH["<<component>><br/>Authentication"]
        end


        subgraph CONTENT_SERVICES["Narration & Content Services"]
            direction LR

            NARRATION["<<component>><br/>Narration Service"]

            LOCALIZATION["<<component>><br/>Localization Service"]

            AUDIO["<<component>><br/>Audio Service"]

            ANALYTICS["<<component>><br/>Analytics Service"]
        end


        %% -------------------------
        %% Component Interfaces
        %% -------------------------

        LOCATION_BRIDGE((Narration<br/>Trigger))

        NARRATION_BRIDGE((Content<br/>Access))

        QR_BRIDGE((POI<br/>Access))

        AUDIO_BRIDGE((Audio<br/>Access))

        ANALYTICS_BRIDGE((Analytics<br/>Event))


        %% -------------------------
        %% Component Communication
        %% ②
        %% -------------------------

        LOCATION -.-> LOCATION_BRIDGE
        LOCATION_BRIDGE -.-> NARRATION

        NARRATION -.-> NARRATION_BRIDGE
        NARRATION_BRIDGE -.-> POI

        NARRATION -.-> LOCALIZATION

        NARRATION -.-> AUDIO_BRIDGE
        AUDIO_BRIDGE -.-> AUDIO

        QR -.-> QR_BRIDGE
        QR_BRIDGE -.-> POI

        LOCATION -.-> ANALYTICS_BRIDGE
        POI -.-> ANALYTICS_BRIDGE
        AUDIO -.-> ANALYTICS_BRIDGE

        ANALYTICS_BRIDGE -.-> ANALYTICS

    end


    %% =========================================================
    %% DATA STORAGE NODE
    %% =========================================================

    subgraph DATA_NODE["<<node>> Data & Storage Server"]
        direction TB

        DATABASE[("Application Database")]

        AUDIO_STORAGE[("Audio Storage")]
    end


    %% =========================================================
    %% TTS NODE
    %% =========================================================

    subgraph TTS_NODE["<<node>> TTS Service"]
        direction TB

        TTS["<<component>><br/>TTS Provider"]
    end


    %% =========================================================
    %% COMMUNICATION BRIDGES BETWEEN NODES
    %% ①
    %% =========================================================

    VISITOR_LINK(("① HTTPS / Network"))
    ADMIN_LINK(("① HTTPS / Network"))

    DATA_LINK(("① Data / Storage Connection"))
    TTS_LINK(("① HTTPS / Network"))


    %% Visitor -> Application Server
    VISITOR_NODE ==>|"① HTTPS / Network"| APP_NODE

    %% Admin -> Application Server
    ADMIN_NODE ==>|"① HTTPS / Network"| APP_NODE

    %% Application Server -> Data Server
    APP_NODE ==>|"① Data / Storage Connection"| DATA_NODE

    %% Application Server -> TTS
    APP_NODE ==>|"① HTTPS / Network"| TTS_NODE


    %% =========================================================
    %% DATA ACCESS INSIDE DEPLOYMENT
    %% =========================================================

    POI -.-> DATABASE
    LOCATION -.-> DATABASE
    AUTH -.-> DATABASE
    LOCALIZATION -.-> DATABASE
    ANALYTICS -.-> DATABASE

    AUDIO -.-> AUDIO_STORAGE
    AUDIO -.-> TTS


    %% =========================================================
    %% LEGEND
    %% =========================================================

    LEGEND_TITLE["Legend"]

    LEGEND_NODE["① Solid / thick line = Communication between nodes"]
    LEGEND_COMPONENT["② Dashed line = Communication between components"]

    LEGEND_TITLE ~~~ LEGEND_NODE
    LEGEND_NODE ~~~ LEGEND_COMPONENT


    %% =========================================================
    %% STYLING
    %% =========================================================

    classDef component fill:#ffffff,stroke:#333333,stroke-width:2px,color:#111111;
    classDef storage fill:#f3f3f3,stroke:#444444,stroke-width:2px,color:#111111;
    classDef bridge fill:#ffffff,stroke:#666666,stroke-width:2px,color:#111111;

    class VISITOR_APP,VISITOR_HARDWARE,ADMIN_CMS,POI,LOCATION,QR,AUTH,NARRATION,LOCALIZATION,AUDIO,ANALYTICS,TTS component;

    class DATABASE,AUDIO_STORAGE,VISITOR_STORAGE storage;

    class LOCATION_BRIDGE,NARRATION_BRIDGE,QR_BRIDGE,AUDIO_BRIDGE,ANALYTICS_BRIDGE,VISITOR_LINK,ADMIN_LINK,DATA_LINK,TTS_LINK bridge;
