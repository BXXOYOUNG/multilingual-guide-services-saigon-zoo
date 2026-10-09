import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';

export default function PublicLayout() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Thảo Cầm Viên</h1>
        <span className="app-badge">PWA Shell</span>
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