// Import React so we can use React features and JSX.
import React from "react";

// Import ReactDOM so React can attach the app to the browser page.
import ReactDOM from "react-dom/client";

// Import the main application component from App.tsx.
import App from "./App";


// Find the HTML element with id="root", create a React root there,
// and render the App component inside it.
ReactDOM.createRoot(document.getElementById("root")!).render(
  // StrictMode helps catch certain issues during development.
  <React.StrictMode>
    <App />
  </React.StrictMode>
);