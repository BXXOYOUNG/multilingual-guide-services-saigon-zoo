import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App';
import './app/index.css';
import { registerServiceWorker } from './sw/registerServiceWorker';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Register PWA Service Worker
registerServiceWorker();

