## Deployment Diagram

```mermaid
flowchart TB

    %% =====================================================
    %% USER DEVICES
    %% =====================================================
    subgraph USER_DEVICES["USER DEVICES"]

        direction TB

        subgraph VISITOR_DEVICE["<<device>> Visitor Mobile Device"]

            VISITOR_APP["<<component>><br/>Visitor App"]

            GPS["GPS"]

            QR_CAMERA["Camera /<br/>QR Scanner"]

            LOCAL_STORAGE[("Local Storage")]

            AUDIO_PLAYER["Audio Player"]

            VISITOR_APP --- GPS
            VISITOR_APP --- QR_CAMERA
            VISITOR_APP --- LOCAL_STORAGE
            VISITOR_APP --- AUDIO_PLAYER
        end


        subgraph ADMIN_DEVICE["<<device>> Admin Workstation"]

            ADMIN_CMS["<<component>><br/>Admin CMS"]

        end
    end


    %% =====================================================
    %% APPLICATION SERVER
    %% =====================================================
    subgraph APP_SERVER["<<node>> Application Server"]

        direction TB

        AUTH["<<component>><br/>Authentication"]

        POI["<<component>><br/>POI Service"]

        LOCATION["<<component>><br/>Location &<br/>Geofence Service"]

        NARRATION["<<component>><br/>Narration Service"]

        QR["<<component>><br/>QR Service"]

        LOCALIZATION["<<component>><br/>Localization Service"]

        AUDIO["<<component>><br/>Audio Service"]

        ANALYTICS["<<component>><br/>Analytics Service"]


        %% ---------------------------------------------
        %% Component communication bridges
        %% ---------------------------------------------

        NARRATION_TRIGGER((Narration<br/>Trigger))

        POI_ACCESS((POI<br/>Access))

        LOCALIZATION_REQUEST((Localization<br/>Request))

        AUDIO_REQUEST((Audio<br/>Request))

        QR_ACCESS((QR<br/>Access))

        OFFLINE_PACKAGE((Offline<br/>Package))

        ANALYTICS_EVENT((Analytics<br/>Event))


        %% ---------------------------------------------
        %% Component communications
        %% ---------------------------------------------

        LOCATION -.-> NARRATION_TRIGGER
        NARRATION_TRIGGER -.-> NARRATION

        NARRATION -.-> POI_ACCESS
        POI_ACCESS -.-> POI

        NARRATION -.-> LOCALIZATION_REQUEST
        LOCALIZATION_REQUEST -.-> LOCALIZATION

        NARRATION -.-> AUDIO_REQUEST
        AUDIO_REQUEST -.-> AUDIO

        QR -.-> QR_ACCESS
        QR_ACCESS -.-> POI

        QR -.-> OFFLINE_PACKAGE
        OFFLINE_PACKAGE -.-> AUDIO

        LOCATION -.-> ANALYTICS_EVENT
        POI -.-> ANALYTICS_EVENT
        AUDIO -.-> ANALYTICS_EVENT

        ANALYTICS_EVENT -.-> ANALYTICS

    end


    %% =====================================================
    %% DATA / STORAGE NODE
    %% =====================================================
    subgraph DATA_NODE["<<node>> Data & Storage Server"]

        DATABASE[("Application Database")]

        AUDIO_STORAGE[("Audio Storage")]

    end


    %% =====================================================
    %% EXTERNAL TTS NODE
    %% =====================================================
    subgraph TTS_NODE["<<node>> TTS Service"]

        TTS["<<component>><br/>TTS Provider"]

    end


    %% =====================================================
    %% HARDWARE / NODE COMMUNICATION
    %% (1)
    %% =====================================================

    VISITOR_DEVICE["Visitor Mobile Device"]
    ADMIN_DEVICE["Admin Workstation"]


    VISITOR_DEVICE ==>|"① Network / HTTPS"| APP_SERVER
    ADMIN_DEVICE ==>|"① Network / HTTPS"| APP_SERVER

    APP_SERVER ==>|"① Database / File Connection"| DATA_NODE
    APP_SERVER ==>|"① Network / HTTPS"| TTS_NODE


    %% =====================================================
    %% COMPONENT DEPENDENCIES TO DATA / EXTERNAL
    %% (2)
    %% =====================================================

    POI -.-> DATABASE
    AUTH -.-> DATABASE
    LOCATION -.-> DATABASE
    LOCALIZATION -.-> DATABASE
    ANALYTICS -.-> DATABASE

    AUDIO -.-> AUDIO_STORAGE
    AUDIO -.-> TTS


    %% =====================================================
    %% LEGEND
    %% =====================================================

    LEGEND1["① Solid line = Hardware / Node communication"]
    LEGEND2["② Dashed line = Component communication"]
    LEGEND3(("Interface / Communication Bridge"))


    LEGEND1 ~~~ LEGEND2
    LEGEND2 ~~~ LEGEND3
