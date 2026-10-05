## Deployment Diagram

```mermaid
flowchart TB

    %% =====================================================
    %% 1. VISITOR DEVICE
    %% =====================================================

    subgraph VISITOR["<<device>> Visitor Mobile Device"]

        direction TB

        V_APP["<<component>><br/>Visitor App"]

        V_GPS["GPS"]

        V_CAMERA["Camera / QR Scanner"]

        V_AUDIO["Audio Player"]

        V_STORAGE[("Local Storage")]

        V_APP --- V_GPS
        V_APP --- V_CAMERA
        V_APP --- V_AUDIO
        V_APP --- V_STORAGE
    end


    %% =====================================================
    %% 2. ADMIN DEVICE
    %% =====================================================

    subgraph ADMIN["<<device>> Admin Workstation"]

        A_CMS["<<component>><br/>Admin CMS"]

    end


    %% =====================================================
    %% 3. APPLICATION SERVER
    %% =====================================================

    subgraph APP["<<node>> Application Server"]

        direction TB

        %% -------------------------------------------------
        %% Core Components
        %% -------------------------------------------------

        subgraph CORE["Core Components"]

            direction TB

            POI["<<component>><br/>POI Service"]

            LOCATION["<<component>><br/>Location &<br/>Geofence Service"]

            QR["<<component>><br/>QR Service"]

            AUTH["<<component>><br/>Authentication"]

        end


        %% -------------------------------------------------
        %% Narration Components
        %% -------------------------------------------------

        subgraph NARRATION_GROUP["Narration Components"]

            direction TB

            NARRATION["<<component>><br/>Narration Service"]

            LOCALIZATION["<<component>><br/>Localization Service"]

            AUDIO["<<component>><br/>Audio Service"]

        end


        %% -------------------------------------------------
        %% Analytics
        %% -------------------------------------------------

        ANALYTICS["<<component>><br/>Analytics Service"]


        %% =================================================
        %% COMPONENT INTERFACES - ②
        %% =================================================

        NARRATION_TRIGGER(("②<br/>Narration Trigger"))

        CONTENT_ACCESS(("②<br/>Content Access"))

        AUDIO_ACCESS(("②<br/>Audio Access"))

        ANALYTICS_EVENT(("②<br/>Analytics Event"))


        %% =================================================
        %% COMPONENT COMMUNICATION
        %% =================================================

        LOCATION -.-> NARRATION_TRIGGER
        NARRATION_TRIGGER -.-> NARRATION

        NARRATION -.-> CONTENT_ACCESS
        CONTENT_ACCESS -.-> POI
        CONTENT_ACCESS -.-> LOCALIZATION

        NARRATION -.-> AUDIO_ACCESS
        AUDIO_ACCESS -.-> AUDIO

        QR -.-> CONTENT_ACCESS

        LOCATION -.-> ANALYTICS_EVENT
        POI -.-> ANALYTICS_EVENT
        AUDIO -.-> ANALYTICS_EVENT

        ANALYTICS_EVENT -.-> ANALYTICS

    end


    %% =====================================================
    %% 4. DATA SERVER
    %% =====================================================

    subgraph DATA["<<node>> Data & Storage Server"]

        direction TB

        DATABASE[("Application Database")]

        AUDIO_STORAGE[("Audio Storage")]

    end


    %% =====================================================
    %% 5. TTS SERVICE
    %% =====================================================

    subgraph TTS_NODE["<<node>> TTS Service"]

        TTS["<<component>><br/>TTS Provider"]

    end


    %% =====================================================
    %% NODE COMMUNICATION - ①
    %% =====================================================

    VISITOR ==>|"① HTTPS / Network"| APP

    ADMIN ==>|"① HTTPS / Network"| APP

    APP ==>|"① Data Connection"| DATA

    APP ==>|"① HTTPS / Network"| TTS_NODE


    %% =====================================================
    %% COMPONENT -> DATA
    %% =====================================================

    POI -.-> DATABASE

    LOCATION -.-> DATABASE

    AUTH -.-> DATABASE

    LOCALIZATION -.-> DATABASE

    ANALYTICS -.-> DATABASE

    AUDIO -.-> AUDIO_STORAGE

    AUDIO -.-> TTS


    %% =====================================================
    %% STYLING
    %% =====================================================

    classDef component fill:#ffffff,stroke:#333333,stroke-width:2px,color:#111111;

    classDef node fill:#fafafa,stroke:#333333,stroke-width:2px,color:#111111;

    classDef storage fill:#f2f2f2,stroke:#555555,stroke-width:2px,color:#111111;

    classDef interface fill:#ffffff,stroke:#555555,stroke-width:2px,color:#111111;


    class V_APP,V_GPS,V_CAMERA,V_AUDIO,A_CMS,POI,LOCATION,QR,AUTH,NARRATION,LOCALIZATION,AUDIO,ANALYTICS,TTS component;

    class DATABASE,AUDIO_STORAGE,V_STORAGE storage;

    class NARRATION_TRIGGER,CONTENT_ACCESS,AUDIO_ACCESS,ANALYTICS_EVENT interface;
