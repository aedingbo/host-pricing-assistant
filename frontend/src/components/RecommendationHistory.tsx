import { useEffect, useState } from "react";
import {
  getRecommendationHistory,
  type RecommendationHistoryRecord,
} from "../api/client";


// Define the props expected by the RecommendationHistory component.
type RecommendationHistoryProps = {
  refreshTrigger: number;
};


// This component retrieves and displays saved recommendation history.
function RecommendationHistory({
  refreshTrigger,
}: RecommendationHistoryProps) {
  // Store the returned history records in React state.
  const [historyRecords, setHistoryRecords] = useState<
    RecommendationHistoryRecord[]
  >([]);

  // Store any error message separately so we can show it in the UI.
  const [errorMessage, setErrorMessage] = useState("");

  // Track whether the history request is currently running.
  const [isLoading, setIsLoading] = useState(true);

  // Load recommendation history when the component first appears
  // and whenever the refresh trigger changes.
  useEffect(() => {
    const loadHistory = async () => {
      setErrorMessage("");
      setIsLoading(true);

      try {
        const records = await getRecommendationHistory();
        setHistoryRecords(records);
      } catch (error) {
        setErrorMessage("Could not load recommendation history.");
        console.error("Recommendation history error:", error);
      } finally {
        setIsLoading(false);
      }
    };

    loadHistory();
  }, [refreshTrigger]);

  return (
    <div>
      <h2>Saved Recommendation History</h2>

      {isLoading && <p>Loading history...</p>}

      {errorMessage && <p>{errorMessage}</p>}

      {!isLoading && !errorMessage && historyRecords.length === 0 && (
        <p>No saved recommendations yet.</p>
      )}

      {!isLoading && !errorMessage && historyRecords.length > 0 && (
        <div>
          {historyRecords.map((record) => (
            <div key={record.id}>
              <h3>
                {record.listing_title} — ${record.recommended_price}
              </h3>
              <p>
                {record.city} | {record.property_type} | {record.beds} bed
                / {record.bathrooms} bath | accommodates {record.accommodates}
              </p>

              <p>
                {record.used_fallback_market_price
                  ? "Estimated Market Price"
                  : "Observed Market Price"}
                : ${record.competitor_avg_price}
              </p>

              <p>{record.explanation}</p>
              <hr />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


export default RecommendationHistory;