import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// This finds the 'root' div in your public/index.html file
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error("Failed to find the root element. Make sure index.html has <div id='root'></div>");
}

const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);