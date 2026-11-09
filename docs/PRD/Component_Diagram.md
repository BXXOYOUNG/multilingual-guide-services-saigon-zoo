@startuml TCV_Component_Diagram
title Component Diagram — Hệ thống thuyết minh đa ngôn ngữ Thảo Cầm Viên

left to right direction
skinparam componentStyle uml2
skinparam packageStyle rectangle
skinparam shadowing false
skinparam defaultFontName SansSerif
skinparam componentBackgroundColor #F3F7F2
skinparam componentBorderColor #426554
skinparam interfaceBorderColor #426554
skinparam packageBorderColor #95A99B
skinparam ArrowColor #52695B

package "Frontend — React PWA" {
  component "Web Application\nGiao diện tham quan / quản trị" as WebApp
  component "Localization\nNgôn ngữ giao diện" as Localization
  component "Map & Geofence\nBản đồ / GPS / vùng kích hoạt" as MapClient
  component "QR Scanner" as QRScanner
  component "Audio & Offline Manager\nPhát / tải / lưu audio và POI\nIndexedDB / Service Worker / Cache" as OfflineAudio
  component "Visitor Tracking\nSự kiện thiết bị / phiên ẩn danh" as Tracking
  component "Admin Translation UI\nChuẩn bị / dịch Chrome / đối chiếu\nChỉnh sửa / xác nhận lưu" as TranslationUI

  interface "ILocalization" as ILocalization
  interface "IMap" as IMap
  interface "IQRScanner" as IQRScanner
  interface "IAudioPlayback" as IPlayback
  interface "IOfflineData" as IOffline
  interface "IVisitorTracking" as ITracking
  interface "IAdminTranslationEditor" as ITranslationEditor

  Localization -- ILocalization
  MapClient -- IMap
  QRScanner -- IQRScanner
  OfflineAudio -- IPlayback
  OfflineAudio -- IOffline
  Tracking -- ITracking
  TranslationUI -- ITranslationEditor

  WebApp ..> ILocalization : <<use>>
  WebApp ..> IMap : <<use>>
  WebApp ..> IQRScanner : <<use>>
  WebApp ..> IPlayback : <<use>>
  WebApp ..> IOffline : <<use>>
  WebApp ..> ITracking : <<use>>
  WebApp ..> ITranslationEditor : <<use>>
  Localization ..> IOffline : <<use>>
  MapClient ..> IPlayback : <<use>>
  MapClient ..> IOffline : <<use>>
  MapClient ..> ITracking : <<use>>
  OfflineAudio ..> ITracking : <<use>>
}

package "Backend — FastAPI modular monolith" {
  component "Content Management\nPOI / catalog / bản dịch\nAPI và POI Repository" as Content
  component "Authentication & RBAC\nĐăng nhập / session / permission" as Auth
  component "Audio Management\nAudio API / Service / Repository\nTask / asset / package / manifest" as Audio
  component "Geofence Provider\nAPI dữ liệu vùng kích hoạt" as Geofence
  component "Analytics\nGhi sự kiện / tổng hợp dashboard" as Analytics
  component "Media Storage Adapter\nS3-compatible provider" as MediaAdapter
  component "Admin Translation API\nNguồn / revision / preview Redis\nXác nhận lưu transaction" as TranslationAPI

  interface "IPOIContentAPI" as IContent
  interface "IAdminSessionAPI" as ISession
  interface "IAuthorization" as IAuthorization
  interface "IAudioAPI" as IAudio
  interface "IGeofenceAPI" as IGeofence
  interface "IEventIngestionAPI" as IEvents
  interface "IAnalyticsQueryAPI" as IAnalytics
  interface "IMediaStorage" as IMedia
  interface "ITranslationPreviewCommitAPI" as ITranslationAPI

  Content -- IContent
  Auth -- ISession
  Auth -- IAuthorization
  Audio -- IAudio
  Geofence -- IGeofence
  Analytics -- IEvents
  Analytics -- IAnalytics
  MediaAdapter -- IMedia
  TranslationAPI -- ITranslationAPI

  Content ..> IAuthorization : <<use>>\nThao tác quản trị
  Content ..> IMedia : <<use>>\nKiểm tra audio trong admin
  Audio ..> IAuthorization : <<use>>\nThao tác quản trị
  Audio ..> IMedia : <<use>>
  Analytics ..> IAuthorization : <<use>>\nTruy vấn dashboard
  TranslationAPI ..> IAuthorization : <<use>>\ncontent:write
}

package "Hạ tầng dữ liệu" {
  component "MongoDB" as MongoDB <<external>>
  component "Redis" as Redis <<external>>
  component "SeaweedFS" as SeaweedFS <<external>>

  interface "IMongoDataAccess" as IMongo
  interface "IRedisSessionAndRateLimit" as IRedis
  interface "IS3ObjectStorage" as IS3

  MongoDB -- IMongo
  Redis -- IRedis
  SeaweedFS -- IS3
}

package "Nền tảng trình duyệt và dịch vụ ngoài" {
  component "Browser APIs" as BrowserAPIs <<external>>
  component "OpenStreetMap Tiles" as OSM <<external>>
  component "Edge TTS" as EdgeTTS <<external>>
  component "Chrome Native Translator\nMô hình tại máy admin desktop" as ChromeTranslator <<external>>

  interface "IGeolocation" as IGeolocation
  interface "ICameraStream" as ICamera
  interface "IRasterTiles" as ITiles
  interface "ISpeechSynthesisProvider" as ITTS
  interface "IOnDeviceTranslation" as INativeTranslation

  BrowserAPIs -- IGeolocation
  BrowserAPIs -- ICamera
  OSM -- ITiles
  EdgeTTS -- ITTS
  ChromeTranslator -- INativeTranslation
}

package "Công cụ chuẩn bị dữ liệu" {
  component "Dataset / Admin / TTS Tools\nCác script chạy chủ động" as DataTools
}

WebApp ..> IContent : <<use>>
WebApp ..> ISession : <<use>>
WebApp ..> IAudio : <<use>>
WebApp ..> IAnalytics : <<use>>
MapClient ..> IContent : <<use>>
MapClient ..> IGeofence : <<use>>
MapClient ..> IGeolocation : <<use>>
MapClient ..> ITiles : <<use>>
QRScanner ..> ICamera : <<use>>
OfflineAudio ..> IAudio : <<use>>
OfflineAudio ..> IContent : <<use>>
Tracking ..> IEvents : <<use>>
WebApp ..> ITranslationAPI : <<use>>
TranslationUI ..> ITranslationAPI : <<use>>\nChuẩn bị và xác nhận lưu
TranslationUI ..> INativeTranslation : <<use>>\nBấm tải mô hình / dịch tại máy

Content ..> IMongo : <<use>>
Auth ..> IMongo : <<use>>
Auth ..> IRedis : <<use>>
Audio ..> IMongo : <<use>>
Audio ..> IRedis : <<use>>\nLease TTS có TTL
Audio ..> ITTS : <<use>>\nAdmin yêu cầu TTS
TranslationAPI ..> IMongo : <<use>>\nNguồn / đích / transaction
TranslationAPI ..> IRedis : <<use>>\nPreview nguồn / revision TTL 30 phút
Geofence ..> IMongo : <<use>>
Analytics ..> IMongo : <<use>>
Analytics ..> IRedis : <<use>>
MediaAdapter ..> IS3 : <<use>>

DataTools ..> IMongo : <<use>>
DataTools ..> IS3 : <<use>>
DataTools ..> ITTS : <<use>>

note bottom of Auth
  Các component backend là module trong cùng ứng dụng FastAPI.
  Interface biểu diễn hợp đồng kiến trúc, không phải class mới trong code.
end note

note bottom of DataTools
  Script seed vẫn có thể gọi Edge TTS khi được chạy chủ động.
  Admin runtime gọi TTS qua FastAPI BackgroundTasks, không có worker bền vững.
end note

note bottom of ChromeTranslator
  Chrome desktop qua localhost hoặc HTTPS, gồm HTTPS tunnel.
  Không cần Cloud API key; cặp không hỗ trợ dùng nhập thủ công.
  Bản dịch mới ở React trước commit; backend không tự dịch hoặc tự tạo TTS.
end note

legend bottom
  Hình chữ nhật có biểu tượng component: thành phần phần mềm.
  Hình tròn nối bằng đường liền: provided interface của component.
  Mũi tên nét đứt <<use>>: component yêu cầu / sử dụng interface.
endlegend
@enduml
