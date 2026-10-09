import React, { useState, useEffect } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { isOnline, subscribeNetworkStatus } from '../../services/networkStatus';

export default function PublicLayout() {
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
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          end
        >
          <span className="nav-icon">🏠</span>
          <span>Trang chủ</span>
        </NavLink>

        <NavLink
          to="/map"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <span className="nav-icon">🗺️</span>
          <span>Bản đồ</span>
        </NavLink>

        <NavLink
          to="/explore"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <span className="nav-icon">🧭</span>
          <span>Khám phá</span>
        </NavLink>

        <NavLink
          to="/admin"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <span className="nav-icon">⚙️</span>
          <span>Quản trị</span>
        </NavLink>
      </nav>
    </div>
  );
}

