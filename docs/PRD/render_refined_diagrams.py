"""Render the as-built UML diagrams to SVG, PNG and editable diagrams.net XML.

Run from any directory: python docs/PRD/render_refined_diagrams.py
Requires Pillow. Coordinates are explicit so routing does not change on export.
"""
from pathlib import Path
from html import escape
import math
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
FONT = Path('C:/Windows/Fonts/arial.ttf')
BOLD = Path('C:/Windows/Fonts/arialbd.ttf')
INK = '#203B45'
MUTED = '#536D78'
GREEN = '#277765'
BLUE = '#346B97'
GOLD = '#9A6926'


class Diagram:
    def __init__(self, name, width, height, title, subtitle):
        self.name, self.width, self.height = name, width, height
        self.svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                    f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
                    '<rect width="100%" height="100%" fill="white"/>']
        self.im = Image.new('RGB', (width * 2, height * 2), 'white')
        self.pen = ImageDraw.Draw(self.im)
        self.model = ET.Element('mxGraphModel', grid='1', gridSize='10', page='1',
                                pageWidth=str(width), pageHeight=str(height))
        self.root = ET.SubElement(self.model, 'root')
        ET.SubElement(self.root, 'mxCell', id='0')
        ET.SubElement(self.root, 'mxCell', id='1', parent='0')
        self.count = 1
        self.routes = []
        self.obstacles = []
        self.text_regions = []
        self.text(40, 38, title, 30, True)
        self.text(40, 82, subtitle, 17, color=MUTED)

    def cell(self, style, x, y, w, h, value=''):
        self.count += 1
        cell = ET.SubElement(self.root, 'mxCell', id=str(self.count), value=value,
                             style=style, vertex='1', parent='1')
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w),
                      height=str(h), **{'as': 'geometry'})

    def text(self, x, y, value, size=17, bold=False, color=INK, max_width=None):
        font = ImageFont.truetype(str(BOLD if bold else FONT), size * 2)
        w = self.pen.textlength(value, font=font) / 2
        if max_width is not None:
            assert w <= max_width, f'Text overflow ({w:.0f}>{max_width}): {value}'
        assert x >= 0 and x + w <= self.width and y + size + 5 <= self.height, value
        self.text_regions.append((x, y, x+w, y+size+2, value))
        self.svg.append(f'<text x="{x}" y="{y + size}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')
        self.pen.text((x * 2, y * 2), value, font=font, fill=color, anchor='lt')
        self.cell(f'text;html=0;align=left;verticalAlign=top;whiteSpace=wrap;overflow=visible;fontFamily=Arial;fontSize={size};fontStyle={1 if bold else 0};fontColor={color};spacing=0;',
                  x, y, math.ceil(w) + 4, size + 8, value)

    def rect(self, x, y, w, h, fill='white', stroke='#A9BCC2', kind='box'):
        assert 0 <= x < x + w <= self.width and 0 <= y < y + h <= self.height
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        self.pen.rounded_rectangle((x*2, y*2, (x+w)*2, (y+h)*2), radius=8, fill=fill, outline=stroke, width=3)
        self.cell(f'rounded=1;arcSize=2;fillColor={fill};strokeColor={stroke};strokeWidth=1.5;', x, y, w, h)
        if kind == 'component':
            for dy in (12, 22):
                self.rect(x+w-27, y+dy, 18, 6, fill, stroke)
        if kind == 'node':
            # Small beveled corner denotes a deployment node; stereotype is explicit.
            self.line([(x+w-22, y), (x+w-22, y+15), (x+w, y+15)], stroke, arrow=False)

    def group(self, x, y, w, h, title, subtitle, fill='#F3F8F7', stroke=GREEN):
        self.rect(x, y, w, h, fill, stroke)
        self.text(x+20, y+15, title, 21, True, stroke, w-40)
        self.text(x+20, y+48, subtitle, 14, color=MUTED, max_width=w-40)

    def box(self, x, y, w, h, title, lines=(), kind='component', stroke=GREEN, size=16):
        self.rect(x, y, w, h, 'white', stroke, kind)
        self.text(x+16, y+11, title, size+1, True, max_width=w-54)
        for n, line in enumerate(lines):
            self.text(x+16, y+39+n*23, line, size-1, color=MUTED, max_width=w-30)
        assert not lines or 39+(len(lines)-1)*23+size+4 <= h, title
        self.obstacles.append((x, y, x+w, y+h))

    def line(self, points, color=BLUE, dashed=False, arrow=True):
        for a, b in zip(points, points[1:]):
            assert a[0] == b[0] or a[1] == b[1], 'Use orthogonal routing'
        pts = ' '.join(f'{x},{y}' for x, y in points)
        dash = ' stroke-dasharray="7 5"' if dashed else ''
        self.svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"{dash} stroke-linejoin="round"/>')
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            length = math.hypot(bx-ax, by-ay)
            if dashed:
                for start in range(0, int(length), 12):
                    end = min(start+7, length)
                    self.pen.line(((ax+(bx-ax)*start/length)*2, (ay+(by-ay)*start/length)*2,
                                   (ax+(bx-ax)*end/length)*2, (ay+(by-ay)*end/length)*2), fill=color, width=4)
            else:
                self.pen.line((ax*2, ay*2, bx*2, by*2), fill=color, width=4)
        if arrow:
            (ax, ay), (bx, by) = points[-2:]
            dx, dy = bx-ax, by-ay
            length = math.hypot(dx, dy)
            ux, uy = dx/length, dy/length
            tri = [(bx, by), (bx-10*ux+5*uy, by-10*uy-5*ux), (bx-10*ux-5*uy, by-10*uy+5*ux)]
            self.svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in tri)}" fill="{color}"/>')
            self.pen.polygon([(x*2, y*2) for x,y in tri], fill=color)
            self.routes.append(points)
        self.count += 1
        cell = ET.SubElement(self.root, 'mxCell', id=str(self.count), parent='1', edge='1',
                             style=f'edgeStyle=none;rounded=0;html=0;strokeColor={color};strokeWidth=2;dashed={int(dashed)};endArrow={"block" if arrow else "none"};endFill=1;')
        geom = ET.SubElement(cell, 'mxGeometry', relative='1', **{'as': 'geometry'})
        ET.SubElement(geom, 'mxPoint', x=str(points[0][0]), y=str(points[0][1]), **{'as': 'sourcePoint'})
        ET.SubElement(geom, 'mxPoint', x=str(points[-1][0]), y=str(points[-1][1]), **{'as': 'targetPoint'})
        arr = ET.SubElement(geom, 'Array', **{'as': 'points'})
        for x, y in points[1:-1]:
            ET.SubElement(arr, 'mxPoint', x=str(x), y=str(y))

    def note(self, x, y, w, title, lines):
        self.text(x, y, title, 18, True, max_width=w)
        for n, line in enumerate(lines):
            self.text(x, y+34+n*26, line, 16, color=MUTED, max_width=w)

    def validate_routes(self):
        segments = [(i, a, b) for i, route in enumerate(self.routes) for a, b in zip(route, route[1:])]
        for i, a, b in segments:
            # Open interiors: entering/leaving a component boundary is allowed.
            for x0, y0, x1, y1 in self.obstacles:
                if a[0] == b[0]:
                    hit = x0 < a[0] < x1 and max(min(a[1],b[1]),y0) < min(max(a[1],b[1]),y1)
                else:
                    hit = y0 < a[1] < y1 and max(min(a[0],b[0]),x0) < min(max(a[0],b[0]),x1)
                assert not hit, f'Route {i} crosses box {(x0,y0,x1,y1)}'
            for x0, y0, x1, y1, value in self.text_regions:
                if a[0] == b[0]:
                    hit = x0 < a[0] < x1 and max(min(a[1],b[1]),y0) < min(max(a[1],b[1]),y1)
                else:
                    hit = y0 < a[1] < y1 and max(min(a[0],b[0]),x0) < min(max(a[0],b[0]),x1)
                assert not hit, f'Route {i} crosses text: {value}'
            for j, c, d in segments:
                if j <= i:
                    continue
                if a[0] == b[0] and c[0] == d[0]:
                    hit = a[0] == c[0] and max(min(a[1],b[1]),min(c[1],d[1])) < min(max(a[1],b[1]),max(c[1],d[1]))
                elif a[1] == b[1] and c[1] == d[1]:
                    hit = a[1] == c[1] and max(min(a[0],b[0]),min(c[0],d[0])) < min(max(a[0],b[0]),max(c[0],d[0]))
                else:
                    v0,v1,h0,h1 = (a,b,c,d) if a[0] == b[0] else (c,d,a,b)
                    hit = min(h0[0],h1[0]) < v0[0] < max(h0[0],h1[0]) and min(v0[1],v1[1]) < h0[1] < max(v0[1],v1[1])
                assert not hit, f'Routes {i} and {j} cross/overlap'

    def save(self):
        self.validate_routes()
        (OUT / f'{self.name}.svg').write_text('\n'.join(self.svg + ['</svg>']), encoding='utf-8')
        self.im.save(OUT / f'{self.name}.png', optimize=True)
        mxfile = ET.Element('mxfile', host='app.diagrams.net', type='device')
        page = ET.SubElement(mxfile, 'diagram', id=self.name, name=self.name)
        page.append(self.model)
        ET.indent(mxfile)
        ET.ElementTree(mxfile).write(OUT / f'{self.name}.drawio', encoding='utf-8', xml_declaration=True)
        print(f'{self.name}: SVG, PNG {self.width*2}x{self.height*2}, drawio; routes validated')


def component():
    d = Diagram('Component_Diagram_Refined', 1800, 1310,
                'COMPONENT DIAGRAM  /  Thuyết minh đa ngôn ngữ Thảo Cầm Viên',
                'Cấu trúc mã nguồn hiện tại • Thành phần lồng trong package • Mũi tên nét đứt: phụ thuộc sử dụng • 13/11/2026')
    d.group(40,150,500,720,'01  FRONTEND · React PWA','frontend/src · Một ứng dụng cho khách và quản trị')
    front = [
        ('Ứng dụng & điều hướng', ['app/ · components/layout/ · components/views/']),
        ('Ngôn ngữ giao diện & nội dung', ['features/localization/ · 6 ngôn ngữ']),
        ('Bản đồ · GPS · geofence · lộ trình', ['features/map/ · MapView · ItineraryView']),
        ('Quét QR & phát thuyết minh', ['features/qr/ · HTML Audio trong các view']),
        ('Audio offline & bộ nhớ tại thiết bị', ['features/offline/ · db/ · sw/ · cacheStorage']),
        ('Quản trị nội dung & dịch tại máy', ['AdminPoiWorkflow · AdminTranslationPanel']),
        ('Theo dõi ẩn danh & dashboard', ['services/analytics.js · AnalyticsDashboard']),
    ]
    for n,(title,lines) in enumerate(front):
        d.box(60,225+n*90,460,72,title,lines)

    d.group(680,150,600,720,'02  BACKEND · FastAPI','backend/ · Modular monolith · Các module cùng một process')
    d.box(700,225,560,100,'Router / hợp đồng HTTP',[
        'api/: pois · geofences · audio · visitor · health',
        'api/: admin · admin_auth · admin_workflow · admin_translation'])
    d.group(700,365,560,265,'Module nghiệp vụ','API gọi service / repository hoặc truy cập DB trực tiếp',fill='#F8FAFC',stroke=BLUE)
    modules = [
        ('POI & geofence',['api/pois.py · api/geofences.py']),
        ('Auth & RBAC',['services/admin_auth.py']),
        ('Audio & gói tải',['services/audio.py · api/audio.py']),
        ('Dịch: preview / commit',['api/admin_translation.py']),
        ('Visitor & analytics',['api/visitor.py · api/admin.py']),
        ('Tạo giọng TTS',['services/admin_narration.py']),
    ]
    for n,(title,lines) in enumerate(modules):
        d.box(715+(n%2)*270,430+(n//2)*65,260,60,title,lines,size=13)
    d.box(700,675,560,80,'Truy cập dữ liệu',[
        'repositories/poi_repository.py · repositories/audio.py',
    ])
    d.box(700,790,560,65,'S3 media adapter & hạ tầng dùng chung',[],size=17)
    d.text(716,825,'services/audio_storage.py · database/ · config · core/',14,color=MUTED,max_width=525)

    d.group(1370,150,390,720,'03  DỮ LIỆU & DỊCH VỤ','Các phụ thuộc của backend',fill='#F3F7FC',stroke=BLUE)
    d.box(1390,225,350,115,'MongoDB · replica set rs0',[
        'POI · bản dịch · geofence · admin',
        'Audio task / asset / package',
        'Thiết bị · phiên · sự kiện · lịch sử'],stroke=BLUE)
    d.box(1390,365,350,115,'Redis',[
        'Auth: session · giới hạn tần suất',
        'TTS: lease 5 phút',
        'Dịch: nguồn / revision, TTL 30 phút'],stroke=BLUE)
    d.box(1390,505,350,115,'SeaweedFS · S3',[
        'MP3 & ảnh POI upload',
        'Được gọi qua media adapter',
        'MongoDB chỉ giữ metadata'],stroke=BLUE)
    d.box(1390,645,350,115,'Edge TTS · dịch vụ ngoài',[
        'Sinh MP3 khi admin yêu cầu',
        'BackgroundTasks trong FastAPI',
        'Script cũng có thể tạo audio'],stroke=BLUE)
    d.text(1390,794,'Mỗi khối ghi rõ dữ liệu / bên sử dụng.',14,color=MUTED,max_width=350)
    d.text(1390,820,'Quan hệ được gom ở biên package.',14,color=MUTED,max_width=350)

    d.group(40,935,500,220,'04  NỀN TẢNG PHÍA CLIENT','Phụ thuộc của frontend · không phải module backend',fill='#FFFAF0',stroke=GOLD)
    d.text(60,1016,'Browser: GPS · camera · HTML Audio · storage',16,max_width=460)
    d.text(60,1048,'Chrome Translator: dịch tại máy admin desktop',16,max_width=460)
    d.text(60,1080,'OpenStreetMap: raster tiles trực tuyến',16,max_width=460)
    d.text(60,1112,'Native model nằm trong Chrome profile',15,color=MUTED,max_width=460)

    d.group(680,935,600,220,'05  CÔNG CỤ CHUẨN BỊ & VẬN HÀNH','scripts/ · Chạy chủ động, tách khỏi request của khách',fill='#FFFAF0',stroke=GOLD)
    d.text(700,1016,'Seed CSV/JSON · tạo admin · đồng bộ dữ liệu ngôn ngữ',16,max_width=560)
    d.text(700,1048,'Tạo MP3 / upload · backup / kiểm tra phục hồi',16,max_width=560)
    d.text(700,1080,'Phụ thuộc: MongoDB · S3 · Edge TTS',16,max_width=560)
    d.text(700,1112,'PowerShell launcher: bật / tắt các tiến trình demo',15,color=MUTED,max_width=560)

    d.line([(540,195),(680,195)],dashed=True)
    d.text(553,165,'HTTP API',14,color=BLUE)
    d.line([(1280,195),(1370,195)],dashed=True)
    d.text(1288,165,'sử dụng',14,color=BLUE)
    d.line([(980,325),(980,365)],dashed=True)
    d.line([(980,630),(980,675)],dashed=True)
    d.line([(290,870),(290,935)],color=GOLD,dashed=True)
    d.text(305,891,'API trình duyệt / tiles',14,color=GOLD)
    d.line([(1280,1040),(1565,1040),(1565,870)],color=GOLD,dashed=True)
    d.text(1340,1060,'seed / media / TTS',15,color=GOLD)
    d.note(40,1190,1720,'Cách đọc & phạm vi',[
        'Ký hiệu component: đơn vị mã nguồn; khung lớn: package. Nhóm nghiệp vụ có thể trải qua cả api/ và services/.',
        'Mũi tên ở biên gom các phụ thuộc cùng đích; không có API gateway hay microservice mới. Chi tiết ánh xạ: DIAGRAMS_REFINED.md.',
        'Geofence xét ở client. Dịch native cần admin xem và xác nhận lưu; dịch không tự sinh TTS. Offline dùng dữ liệu đã tải trước.',
    ])
    d.save()


def deployment():
    d = Diagram('Deployment_Diagram_Refined',1800,1450,
                'DEPLOYMENT DIAGRAM  /  Thuyết minh đa ngôn ngữ Thảo Cầm Viên',
                'Hạ tầng demo hiện tại • Node / runtime / artifact / lưu trữ • Mũi tên: bên khởi tạo kết nối; phản hồi đi ngược lại • 13/11/2026')
    d.group(40,150,390,310,'THIẾT BỊ TỪ XA','«device» Điện thoại / máy tính khách hoặc admin',stroke=GREEN)
    d.box(60,225,350,90,'«browser» React PWA',[
        'Camera · GPS · HTML Audio',
        'Chrome desktop: native Translator'],kind='node')
    d.box(60,355,350,85,'«local storage»',[
        'IndexedDB: POI / ngôn ngữ / MP3 / gói',
        'Cache Storage: shell / JS / CSS / ảnh'],kind='box',size=15)
    d.line([(230,315),(230,355)],color=GREEN)

    d.box(500,190,270,120,'Cloudflare',[
        'Quick Tunnel · HTTPS :443',
        '*.trycloudflare.com',
        'URL tạm thời'],kind='node',stroke=BLUE,size=15)

    d.group(820,150,940,1180,'MÁY HOST WINDOWS','«device» Một bản hệ thống · frontend / backend trên host; dependency trong Docker',stroke=GREEN)
    d.box(850,245,260,125,'«container» cloudflared',[
        'Docker Desktop / Linux',
        'Connector mở tunnel đi ra',
        'host.docker.internal:3000'],kind='node',stroke=BLUE,size=15)
    d.box(1180,245,540,145,'«execution environment» Node.js / Vite',[
        'Preview bind 0.0.0.0:3000',
        '«artifact» frontend/dist · manifest.json · sw.js',
        'Proxy /api/* và /audio/* → 127.0.0.1:8000'],kind='node',size=16)

    d.box(850,480,260,210,'«browser» Local',[
        'http://localhost:3000',
        'React PWA khách / admin',
        'IndexedDB + Cache Storage',
        'ID ẩn danh: local/session',
        'Native Translator (Chrome)',
        'Model trong Chrome profile'],kind='node',size=15)
    d.box(1180,480,540,210,'«execution environment» Python / Uvicorn',[
        'FastAPI · bind 127.0.0.1:8000',
        '«artifact» backend.main:app',
        'POI / geofence / audio / visitor / admin / analytics',
        'Auth cookie HTTP-only + RBAC',
        'Dịch: preview / commit; TTS: BackgroundTasks'],kind='node',size=16)

    d.rect(850,825,870,310,fill='#F3F7FC',stroke=BLUE)
    d.text(1165,1043,'DOCKER DESKTOP',18,True,BLUE,max_width=230)
    d.text(1165,1075,'Linux containers',14,color=MUTED)
    d.text(1165,1100,'Cổng host: 127.0.0.1',14,color=MUTED)
    d.box(870,865,260,160,'«container» MongoDB 6',[
        'mongod :27018 · replica set rs0',
        'saigon-zoo-t10-replset',
        'DB: saigon_zoo_tcv_dataset_dev',
        'Metadata / nội dung / analytics'],kind='node',stroke=BLUE,size=14)
    d.box(1150,865,260,160,'«container» Redis 7',[
        ':6379 · redis:7.0-alpine',
        'saigon-zoo-redis',
        'Session / rate limit / TTS lease',
        'Nguồn & revision preview dịch'],kind='node',stroke=BLUE,size=14)
    d.box(1430,865,270,160,'«container» SeaweedFS',[
        'mini -dir=/data · S3 HTTP :8333',
        'saigon-zoo-t10-seaweedfs',
        'Bucket MP3 / ảnh POI',
        'Truy cập qua backend'],kind='node',stroke=BLUE,size=14)
    d.box(870,1060,260,55,'«volume» DB + config',[],kind='box',stroke=BLUE,size=14)
    d.text(885,1090,'/data/db · /data/configdb',12,color=MUTED)
    d.box(1430,1060,270,55,'«volume» Media',[],kind='box',stroke=BLUE,size=14)
    d.text(1445,1090,'/data · MP3 / ảnh / storage metadata',12,color=MUTED)
    d.line([(1000,1025),(1000,1060)])
    d.line([(1565,1025),(1565,1060)])

    d.box(850,1200,870,100,'«artifact» Công cụ vận hành trên host',[
        'start_demo.ps1 / stop_demo.ps1: điều khiển Vite, Uvicorn và tunnel',
        'Python scripts + data/dataset/: seed / admin / Edge TTS / upload / backup / kiểm tra phục hồi'],kind='box',stroke=GOLD,size=15)
    d.line([(1285,1200),(1285,1135)],color=GOLD,dashed=True)
    d.text(1300,1155,'seed / backup dữ liệu & media',14,color=GOLD)

    d.box(40,540,390,110,'«external» OpenStreetMap',[
        'tile.openstreetmap.org · HTTPS',
        'Client tải raster tiles trực tiếp'],kind='node',stroke=BLUE)
    d.box(40,1260,720,95,'«external» Edge TTS',[
        'Internet khi tạo MP3 · backend hoặc script gọi',
        'Tác vụ admin chạy trong process FastAPI'],kind='node',stroke=BLUE,size=16)
    # Main request path, with separate tracks for local traffic and tile requests.
    d.line([(430,260),(500,260)])
    d.text(437,222,'HTTPS',13,color=BLUE)
    # The connector initiates the encrypted tunnel, even though requests arrive from Cloudflare.
    d.line([(850,290),(770,290)])
    d.text(777,320,'Tunnel',13,color=BLUE)
    d.line([(1110,285),(1180,285)])
    d.text(1117,255,'HTTP',13,color=BLUE)
    d.line([(1110,530),(1145,530),(1145,355),(1180,355)])
    d.text(1100,408,'HTTP',13,color=BLUE)
    d.line([(1450,390),(1450,480)])
    d.text(1465,420,'HTTP :8000 · REST JSON / audio / media',14,color=BLUE)
    d.line([(1240,690),(1240,720),(1000,720),(1000,865)])
    d.text(850,744,'MongoDB TCP :27018',14,color=BLUE)
    d.line([(1450,690),(1450,750),(1280,750),(1280,865)])
    d.text(1150,744,'Redis TCP :6379',14,color=BLUE)
    d.line([(1660,690),(1660,720),(1565,720),(1565,865)])
    d.text(1580,744,'S3 HTTP :8333',14,color=BLUE)
    d.line([(1720,570),(1740,570),(1740,1345),(780,1345),(780,1305),(760,1305)])
    d.text(1200,1308,'Internet · tạo MP3 qua Edge TTS',14,color=BLUE)
    d.line([(230,460),(230,540)])
    d.text(245,490,'HTTPS tiles',14,color=BLUE)
    d.line([(850,610),(790,610),(790,590),(430,590)])
    d.text(505,558,'HTTPS tiles từ browser local',14,color=BLUE)

    d.note(40,740,720,'LUỒNG RUNTIME',[
        '1. Khách từ xa → HTTPS Cloudflare → tunnel → Vite.',
        '   cloudflared mở kết nối mã hóa đi ra Cloudflare.',
        '2. Vite trả frontend build; /api và /audio được proxy sang FastAPI.',
        '3. FastAPI dùng MongoDB, Redis, S3 qua cổng loopback của host.',
        '4. TTS: admin yêu cầu → FastAPI gọi Edge TTS → MP3 vào S3;',
        '   metadata và trạng thái vào MongoDB; Redis giữ lease tạm.',
        '5. Dịch: API giữ preview → Chrome dịch → admin duyệt → API',
        '   commit transaction MongoDB. Mô hình thuộc Chrome profile.',
    ])
    d.note(40,1030,720,'NGOẠI TUYẾN & PHẠM VI TRIỂN KHAI',[
        'Dùng POI / gói / audio đã tải và shell đã cache trên cùng origin.',
        'Đổi URL tunnel tạo origin khác; OSM vẫn cần mạng.',
        'GPS / camera cần quyền browser và localhost hoặc HTTPS.',
        'Native translation tùy Chrome desktop / cặp ngôn ngữ;',
        'không hỗ trợ thì nhập tay. Tải model lần đầu cần Internet.',
        'Backup DB / media tách khỏi Git; mỗi máy chạy bản riêng.',
        'Script chuẩn bị có thể gọi Edge TTS trực tiếp như backend.',
    ])
    d.note(40,1360,1720,'Ký hiệu UML & ranh giới',[
        '«device»: máy vật lý · «execution environment» / «container» / «browser»: môi trường thực thi · «artifact»: bản build / mã triển khai.',
        'Đường liền: kết nối runtime / lưu trữ; nét đứt: vận hành. Frontend và FastAPI ở host; dữ liệu không công khai qua tunnel. Không có worker TTS bền vững.',
    ])
    d.save()


if __name__ == '__main__':
    component()
    deployment()
