import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFoundView() {
  return (
    <div className="card" style={{ textAlign: 'center' }}>
      <h2>404 - Không tìm thấy trang</h2>
      <p style={{ marginBottom: '16px' }}>Đường dẫn không tồn tại trên hệ thống.</p>
      <Link to="/" className="btn">
        Về trang chủ
      </Link>
    </div>
  );
}

