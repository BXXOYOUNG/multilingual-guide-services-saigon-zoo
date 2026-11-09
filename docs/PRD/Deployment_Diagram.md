@startuml TCV_Current_Deployment_Diagram
title Deployment Diagram — Thuyết minh đa ngôn ngữ Thảo Cầm Viên\nMôi trường demo Windows + Docker Desktop — 09/11/2026

left to right direction
skinparam shadowing false
skinparam defaultFontName SansSerif
skinparam ArrowColor #426554
skinparam nodeBackgroundColor #F4F8F0
skinparam nodeBorderColor #426554
skinparam databaseBackgroundColor #EDF3FA
skinparam databaseBorderColor #627E9B
skinparam artifactBackgroundColor #FFFFFF
skinparam noteBackgroundColor #FFF6DB
skinparam noteBorderColor #CFB675

node "Thiết bị từ xa\nĐiện thoại / máy tính của khách hoặc admin" as RemoteDevice {
  node "Trình duyệt / PWA đã cài\nCamera · Geolocation · HTML Audio" as RemoteBrowser {
    artifact "React visitor UI + admin UI\nCùng một frontend" as RemoteApp
    database "Lưu tại thiết bị\nIndexedDB: ngôn ngữ / POI / gói / audio\nCache Storage: shell / ảnh / font / JS\nlocalStorage / sessionStorage: ID ẩn danh" as RemoteCache
    RemoteApp --> RemoteCache
    artifact "Native Translator API (nếu Chrome desktop)\nMô hình do Chrome quản lý trong profile" as RemoteTranslator
    RemoteApp --> RemoteTranslator : admin bấm dịch tại máy
  }
}

cloud "Cloudflare Quick Tunnel\nURL HTTPS tạm: *.trycloudflare.com" as Cloudflare
cloud "OpenStreetMap\ntile.openstreetmap.org\nRaster tile HTTPS" as OSM
cloud "Edge TTS\nOnline, dùng khi tạo audio" as EdgeTTS

node "Máy host Windows\nMáy đang vận hành một bản hệ thống" as Host {
  node "Trình duyệt local\nKhách / quản trị" as LocalBrowser {
    artifact "React PWA\nhttp://localhost:3000" as LocalApp
    database "IndexedDB + Cache Storage\nlocalStorage + sessionStorage" as LocalCache
    LocalApp --> LocalCache
    artifact "Native Chrome Translator API\nMô hình trong Chrome profile, không thuộc IndexedDB app" as LocalTranslator
    LocalApp --> LocalTranslator : admin bấm dịch tại máy
  }

  node "Node.js / Vite preview\nBind 0.0.0.0:3000" as Frontend {
    artifact "frontend/dist\nHTML · JS · CSS · ảnh · font\nmanifest.json · sw.js" as FrontendBuild
    artifact "Vite proxy\n/api/* và /audio/*\n=> http://127.0.0.1:8000" as Proxy
  }

  node "Python / Uvicorn\nBind 127.0.0.1:8000" as Backend {
    artifact "FastAPI modular monolith\nbackend.main:app\nPOI · geofence · audio · visitor events\nAdmin auth / RBAC · nội dung · analytics" as API
  }

  node "Công cụ vận hành trên host" as Tools {
    artifact "PowerShell launcher\nstart_demo.ps1 / stop_demo.ps1" as Launcher
    artifact "Python scripts chạy chủ động\nSeed / tạo Edge TTS / create_admin\nBackup / kiểm tra phục hồi" as Maintenance
    artifact "Dữ liệu nguồn\ndata/dataset/*.csv và *.json" as SourceDataset
    SourceDataset --> Maintenance
  }

  node "Docker Desktop / Linux containers" as Docker {
    node "saigon-zoo-demo-tunnel\ncloudflare/cloudflared" as TunnelContainer {
      artifact "cloudflared connector\n--url http://host.docker.internal:3000" as Connector
    }

    node "saigon-zoo-t10-replset\nmongo:6.0" as MongoContainer {
      database "mongod :27018\nReplica set rs0\nDB: saigon_zoo_tcv_dataset_dev" as MongoDB
    }

    node "saigon-zoo-redis\nredis:7.0-alpine" as RedisContainer {
      database "Redis :6379\nSession / rate limit / lease TTS\nToken nguồn và revision preview dịch" as Redis
    }

    node "saigon-zoo-t10-seaweedfs\nSeaweedFS mini -dir=/data" as SeaweedContainer {
      artifact "S3-compatible endpoint :8333\nBucket chứa MP3 và ảnh upload" as S3
    }

    storage "Docker persistent volumes\nTách khỏi source Git" as Volumes {
      artifact "MongoDB data + config\nMount /data/db và /data/configdb" as MongoVolume
      artifact "SeaweedFS data\nMount /data" as MediaVolume
    }

    MongoDB --> MongoVolume : lưu database
    S3 --> MediaVolume : lưu audio và metadata storage
  }
}

RemoteApp --> Cloudflare : HTTPS / 443\nHTML, asset, /api, /audio
Cloudflare <--> Connector : Cloudflare Tunnel mã hóa\nconnector mở kết nối đi ra
Connector --> Frontend : HTTP / host.docker.internal:3000
LocalApp --> Frontend : HTTP / localhost:3000
FrontendBuild ..> RemoteApp : tải frontend và service worker
FrontendBuild ..> LocalApp : tải frontend và service worker
Proxy --> API : HTTP / 127.0.0.1:8000\nREST JSON và audio response

API --> MongoDB : MongoDB wire protocol\n127.0.0.1:27018 => container:27018
API --> Redis : Redis protocol\n127.0.0.1:6379 => container:6379
API --> S3 : S3 qua HTTP\n127.0.0.1:8333 => container:8333
API --> EdgeTTS : Internet khi admin yêu cầu\nFastAPI BackgroundTasks tạo MP3

RemoteApp --> OSM : tải nền bản đồ trực tiếp
LocalApp --> OSM : tải nền bản đồ trực tiếp
Maintenance --> EdgeTTS : tạo MP3 khi chuẩn bị dữ liệu
Maintenance --> MongoDB : host 127.0.0.1:27018\nseed / admin / audio metadata
Maintenance --> S3 : host 127.0.0.1:8333\nupload audio
Launcher ..> Frontend : build / mở / dừng preview
Launcher ..> Backend : mở / dừng Uvicorn
Launcher ..> TunnelContainer : tạo / dừng tunnel

note bottom of Launcher
  Cần bật MongoDB, Redis và SeaweedFS trước khi chạy launcher.
  -NoTunnel: chạy local, không tạo tunnel mới.
  Frontend dev có thể dùng Vite dev thay preview;
  demo offline dùng production build + preview.
end note

note bottom of Docker
  Publish dependency ports trên 127.0.0.1 của Windows host.
  MongoDB rs0 hiện quảng bá member localhost:27018.
  Frontend và FastAPI chạy trên host, không nằm trong Docker.
  MongoDB/Redis/S3 không được đưa trực tiếp lên Quick Tunnel.
end note

note bottom of RemoteDevice
  HTTPS cho camera/GPS trên thiết bị từ xa, theo quyền browser.
  Offline chỉ dùng dữ liệu đã lưu trên cùng origin và trình duyệt.
  URL tunnel đổi thì storage của origin cũ không tự chuyển.
  Nền OSM online chưa có bộ bản đồ offline đầy đủ.
end note

note right of Maintenance
  Script có thể tạo TTS; admin cũng yêu cầu TTS từ giao diện.
  Không có worker TTS bền vững hoặc Cloud Translation API.
  Backup được gửi riêng; không chứa trong repository Git.
end note

note bottom of LocalTranslator
  Native translation hỗ trợ theo Chrome desktop/cặp ngôn ngữ;
  điện thoại hoặc browser không hỗ trợ dùng nhập thủ công.
  Mô hình cần Internet khi tải lần đầu, không nằm trong gói audio.
  API giữ nguồn/revision trong Redis, rồi lưu bản admin xác nhận vào MongoDB.
  localhost và HTTPS tunnel đều dùng được, không cần API key.
end note

legend bottom
  Đường liền: luồng dữ liệu / kết nối đang được triển khai.
  Đường nét đứt: phân phối artifact hoặc điều khiển tiến trình.
  Cookie admin: HTTP-only, Redis session; Secure khi chạy HTTPS.
  Mỗi máy nhận backup chạy một bản riêng, không tự đồng bộ database.
endlegend
@enduml
