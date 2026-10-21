import React, { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

async function loadDashboard() {
  const response = await fetch('/api/admin/analytics/summary', { credentials: 'same-origin' });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    if (response.status === 401) throw new Error('Phiên đăng nhập đã hết hạn. Hãy đăng nhập lại trong trang quản trị.');
    if (response.status === 403) throw new Error('Tài khoản chưa được cấp quyền xem phân tích.');
    throw new Error(body.error?.message || body.detail || `Máy chủ chưa tải được dashboard (${response.status}). Hãy thử làm mới sau.`);
  }
  return response.json();
}

const EVENT_LABELS = {
  session_start: 'Phiên truy cập', page_view: 'Lượt xem trang', heartbeat: 'Thiết bị hoạt động', poi_view: 'Xem điểm tham quan',
  qr_scan: 'Quét QR', playback_start: 'Bắt đầu audio', playback_complete: 'Nghe hoàn tất', geofence_enter: 'Vào vùng POI', geofence_exit: 'Rời vùng POI',
};
const LANGUAGE_LABELS = { vi: 'Tiếng Việt', en: 'English', fr: 'Français', 'zh-Hans': '中文', ja: '日本語', ko: '한국어', unknown: 'Khác' };

export default function AnalyticsDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [updatedAt, setUpdatedAt] = useState(null);
  const refresh = useCallback(async () => {
    try { const result = await loadDashboard(); setData(result); setError(''); setUpdatedAt(new Date()); }
    catch (cause) { setError(cause.message); }
  }, []);
  useEffect(() => { refresh(); const timer = window.setInterval(refresh, 60_000); return () => window.clearInterval(timer); }, [refresh]);

  const dailyMax = Math.max(1, ...(data?.daily_visits || []).map((item) => item.visits));
  const hourlyMax = Math.max(1, ...(data?.hourly_visits || []).map((item) => item.visits));
  return <section className="analytics-dashboard">
    <div className="dashboard-heading"><div><span className="eyebrow">SAIGON ZOO · ANALYTICS</span><h1>Dashboard thống kê</h1><p>Theo dõi lượng truy cập và mức độ sử dụng hướng dẫn đa ngôn ngữ.</p></div><div className="dashboard-actions"><button type="button" className="btn btn-secondary" onClick={refresh}>Làm mới</button><Link className="btn btn-secondary" to="/admin">Quản lý nội dung</Link></div></div>
    {error && <div className="dashboard-error" role="alert">{error}</div>}
    {!data && !error && <div className="card">Đang tải số liệu…</div>}
    {data && <>
      <div className="dashboard-updated">Cập nhật lúc {updatedAt?.toLocaleTimeString('vi-VN')} · tự làm mới mỗi phút · thời gian thống kê theo UTC</div>
      <div className="dashboard-kpis">
        <article className="dashboard-kpi live"><span>Thiết bị hoạt động</span><strong>{data.active_devices}</strong><small>Có sự kiện trong 5 phút gần nhất</small></article>
        <article className="dashboard-kpi"><span>Lượt truy cập hôm nay</span><strong>{data.visits_today}</strong><small>Phiên mới trong ngày UTC</small></article>
        <article className="dashboard-kpi"><span>Tổng lượt truy cập</span><strong>{data.visits_total}</strong><small>Từ khi bật ghi nhận truy cập</small></article>
        <article className="dashboard-kpi"><span>Sự kiện hôm nay</span><strong>{data.events_today}</strong><small>{data.total_events} sự kiện toàn thời gian</small></article>
        <article className="dashboard-kpi"><span>Lượt bắt đầu nghe</span><strong>{data.audio_starts_today}</strong><small>Hoàn tất {data.audio_completions_today} · tỷ lệ {data.audio_completion_rate_today}%</small></article>
      </div>
      <div className="dashboard-grid">
        <article className="dashboard-panel dashboard-chart"><div className="dashboard-panel-heading"><div><h2>Lượt truy cập 7 ngày</h2><p>Số phiên bắt đầu mỗi ngày</p></div></div><div className="bar-chart daily-chart">{data.daily_visits.map((item) => <div className="bar-column" key={item.date} title={`${item.date}: ${item.visits}`}><span>{item.visits}</span><div style={{ height: `${Math.max(5, item.visits / dailyMax * 100)}%` }} /><small>{item.date.slice(5)}</small></div>)}</div></article>
        <article className="dashboard-panel dashboard-chart"><div className="dashboard-panel-heading"><div><h2>Khung giờ hôm nay</h2><p>Lượt bắt đầu phiên theo giờ UTC</p></div></div><div className="bar-chart hourly-chart">{Array.from({ length: 24 }, (_, hour) => { const value = data.hourly_visits.find((item) => item.hour === hour)?.visits || 0; return <div className="bar-column" key={hour} title={`${String(hour).padStart(2, '0')}:00 · ${value}`}><div style={{ height: `${Math.max(value ? 5 : 2, value / hourlyMax * 100)}%` }} /><small>{hour % 4 === 0 ? `${String(hour).padStart(2, '0')}h` : ''}</small></div>; })}</div></article>
        <article className="dashboard-panel"><div className="dashboard-panel-heading"><div><h2>Điểm tham quan nổi bật</h2><p>Lượt xem, quét QR và bắt đầu audio hôm nay</p></div></div>{data.top_pois.length ? <ol className="dashboard-ranking">{data.top_pois.map((item) => <li key={item.poi_id}><span>{item.name}</span><strong>{item.interactions}</strong></li>)}</ol> : <p className="dashboard-empty">Chưa có tương tác POI hôm nay.</p>}</article>
        <article className="dashboard-panel"><div className="dashboard-panel-heading"><div><h2>Ngôn ngữ sử dụng</h2><p>Lượt xem, quét QR và nghe audio theo ngôn ngữ</p></div></div>{data.languages_today.length ? <ul className="dashboard-ranking">{data.languages_today.map((item) => <li key={item.language}><span>{LANGUAGE_LABELS[item.language] || item.language}</span><strong>{item.visits}</strong></li>)}</ul> : <p className="dashboard-empty">Chưa có hoạt động theo ngôn ngữ hôm nay.</p>}</article>
        <article className="dashboard-panel dashboard-events"><div className="dashboard-panel-heading"><div><h2>Hoạt động hôm nay</h2><p>Phân loại sự kiện đã ghi nhận</p></div></div>{data.event_counts.length ? <ul className="dashboard-ranking">{data.event_counts.map((item) => <li key={item.event_type}><span>{EVENT_LABELS[item.event_type] || item.event_type}</span><strong>{item.count}</strong></li>)}</ul> : <p className="dashboard-empty">Chưa có dữ liệu.</p>}</article>
      </div>
      <p className="dashboard-footnote">Số liệu được tổng hợp từ các sự kiện trình duyệt gửi về. Thiết bị hoạt động là ước tính từ heartbeat gần đây; trình chặn theo dõi, chế độ riêng tư hoặc mất mạng có thể làm số liệu thấp hơn thực tế. Chỉ số lịch sử bắt đầu tích lũy từ phiên bản có ghi nhận analytics.</p>
    </>}
  </section>;
}
