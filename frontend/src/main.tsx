import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

console.log('start up frontend with version 3.0.1')
console.log('target host for rest-api: ', window.ENV.VITE_MODEL_API_HOST)
console.log('target port for rest-api: ', window.ENV.VITE_MODEL_API_PORT)
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
