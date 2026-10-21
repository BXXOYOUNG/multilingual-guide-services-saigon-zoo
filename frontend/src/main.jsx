import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App';
import './app/index.css';
import './app/admin.css';
import { registerServiceWorker } from './sw/registerServiceWorker';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// The worker caches Vite modules in demo mode and the complete build in production.
registerServiceWorker();
