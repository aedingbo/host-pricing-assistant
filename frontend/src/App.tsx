import { useState } from "react";
import { getBackendHealth } from "./api/client";
import PricingForm from "./components/PricingForm";
import RecommendationHistory from "./components/RecommendationHistory";


// This is the main top-level React component for the frontend.
function App() {
  // Store the backend response message in React state.
  const [healthMessage, setHealthMessage] = useState("");

  // Store any error message separately so we can show it in the UI.
  const [errorMessage, setErrorMessage] = useState("");

  // Track whether the backend health request is currently running.
  const [isLoading, setIsLoading] = useState(false);

  // Track whether recommendation history should be visible.
  const [showHistory, setShowHistory] = useState(true);

  // Track when history should refresh.
  // Each successful form submission will increase this value.
  const [historyRefreshCount, setHistoryRefreshCount] = useState(0);

  // This function calls the frontend API helper instead of calling fetch directly.
  const checkBackendHealth = async () => {
    // Clear old messages before starting a new request.
    setHealthMessage("");
    setErrorMessage("");
    setIsLoading(true);

    try {
      // Call the reusable API function from client.ts.
      const data = await getBackendHealth();

      // Save the returned status into state so it appears on the page.
      setHealthMessage(data.status);
    } catch (error) {
      // If something goes wrong, show an error message.
      setErrorMessage("Could not connect to the backend.");

      // Log the real error to the browser console for debugging.
      console.error("Backend connection error:", error);
    } finally {
      // Stop the loading state whether the request succeeded or failed.
      setIsLoading(false);
    }
  };

  // This function is called after a recommendation is successfully created.
  // Increasing the refresh counter tells the history component to reload.
  const handleRecommendationCreated = () => {
    setHistoryRefreshCount((previousCount) => previousCount + 1);
  };

  return (
    <div>
      {/* Main heading shown on the page */}
      <h1>Host Pricing Assistant</h1>

      {/* Simple paragraph to confirm the frontend is rendering */}
      <p>Frontend setup is working.</p>

      {/* Button to test the backend connection */}
      <button onClick={checkBackendHealth} disabled={isLoading}>
        {isLoading ? "Checking..." : "Check Backend Health"}
      </button>

      {/* Show the backend success message if we have one */}
      {healthMessage && <p>Backend status: {healthMessage}</p>}

      {/* Show the error message if the request fails */}
      {errorMessage && <p>{errorMessage}</p>}

      <hr />

      {/* Render the host pricing input form */}
      <PricingForm onRecommendationCreated={handleRecommendationCreated} />

      <hr />

      {/* Toggle button for recommendation history */}
      <button onClick={() => setShowHistory((previousValue) => !previousValue)}>
        {showHistory ? "Hide Recommendation History" : "Show Recommendation History"}
      </button>

      <br />
      <br />

      {/* Render saved recommendation history only when visible */}
      {showHistory && (
        <RecommendationHistory refreshTrigger={historyRefreshCount} />
      )}
    </div>
  );
}


export default App;