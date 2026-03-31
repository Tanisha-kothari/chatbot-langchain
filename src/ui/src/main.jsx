import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// Find the div with id="app" in index.html
const root = ReactDOM.createRoot(document.getElementById("app"));

// Render your App component into that div
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);