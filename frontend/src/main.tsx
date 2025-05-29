import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

console.log('target url for rest-api: ', window.ENV.VITE_MODEL_API_URL)
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
