import React, { useState, useEffect } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { useLanguage } from '../../features/localization/LanguageContext';
import {
  isOnline,
  subscribeNetworkStatus,
} from '../../services/networkStatus';

export default function PublicLayout() {
  const {
    currentLanguageInfo,
    isLoadingLanguage,
    openLanguageSelector,
  } = useLanguage();

  const [online, setOnline] = useState(isOnline());

  useEffect(() => {
    return subscribeNetworkStatus(({ online: newStatus }) => {
      setOnline(newStatus);
    });
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Thảo Cầm Viên</h1>
        <button
          type="button"
          className="app-badge app-language-button"
          onClick={openLanguageSelector}
          disabled={isLoadingLanguage}
          aria-label="Chọn ngôn ngữ thuyết minh"
        >
          {isLoadingLanguage
            ? '...'
            : `${currentLanguageInfo?.flag || ''} ${currentLanguageInfo?.nativeName || 'Ngôn ngữ'}`}
        </button>
        <span
          className="app-badge"
          style={{ backgroundColor: online ? 'rgba(255, 255, 255, 0.2)' : '#d32f2f' }}
        >
          {online ? 'Online' : 'Offline'}
        </span>
      </header>

      <main className="app-main">
        <Outlet />
      </main>

      <nav className="app-bottom-nav">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `nav-item ${isActive ? 'active' : ''}`
          }
        >
          <span className="nav-icon">🏠</span>
          <span>Trang chủ</span>
        </NavLink>

        <NavLink
          to="/map"
          className={({ isActive }) =>
            `nav-item ${isActive ? 'active' : ''}`
          }
        >
          <span className="nav-icon">🗺️</span>
          <span>Bản đồ</span>
        </NavLink>

        <NavLink
          to="/explore"
          className={({ isActive }) =>
            `nav-item ${isActive ? 'active' : ''}`
          }
        >
          <span className="nav-icon">🧭</span>
          <span>Khám phá</span>
        </NavLink>

        <NavLink
          to="/admin"
          className={({ isActive }) =>
            `nav-item ${isActive ? 'active' : ''}`
          }
        >
          <span className="nav-icon">⚙️</span>
          <span>Quản trị</span>
        </NavLink>
      </nav>
    </div>
  );
}
