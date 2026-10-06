import React from 'react';
import { Outlet, Link } from 'react-router-dom';

export default function AdminLayout() {
  return (
    <div className="admin-container">
      <header className="admin-header">
        <div>
          <h2>Quản trị Thảo Cầm Viên</h2>
          <p style={{ fontSize: '0.875rem', color: '#666' }}>Hệ thống quản lý nội dung thuyết minh</p>
        </div>
        <div>
          <Link to="/" className="btn btn-secondary">
            Về ứng dụng
          </Link>
        </div>
      </header>

      <main>
        <Outlet />
      </main>
    </div>
  );
}

