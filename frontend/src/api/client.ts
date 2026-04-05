// Base URL for the FastAPI backend during local development.
const API_BASE_URL = "http://127.0.0.1:8000";


// Define the expected shape of the health-check response.
// This helps TypeScript understand what the backend should return.
export type HealthResponse = {
  status: string;
};


// Define the frontend form data shape.
// This matches the fields used in the React form component.
export type PricingFormData = {
  listingTitle: string;
  city: string;
  propertyType: string;
  beds: string;
  bathrooms: string;
  accommodates: string;
  competitorAvgPrice: string;
};


// Define the expected shape of the recommendation response
// returned by the backend.
export type RecommendationResponse = {
  recommended_price: number;
  explanation: string;
};


// Define the expected shape of a saved recommendation history record.
export type RecommendationHistoryRecord = {
  id: number;
  listing_title: string;
  city: string;
  property_type: string;
  beds: number;
  bathrooms: number;
  accommodates: number;
  competitor_avg_price: number;
  used_fallback_market_price: boolean;
  recommended_price: number;
  explanation: string;
};


// Create a reusable function for checking backend health.
export async function getBackendHealth(): Promise<HealthResponse> {
  // Send a GET request to the backend health endpoint.
  const response = await fetch(`${API_BASE_URL}/health`);

  // If the response is not successful, throw an error.
  // This lets the calling code handle the failure in one place.
  if (!response.ok) {
    throw new Error("Backend health request failed.");
  }

  // Convert the response body from JSON into JavaScript data.
  return response.json();
}


// Create a reusable function for requesting a pricing recommendation.
export async function createRecommendation(
  formData: PricingFormData
): Promise<RecommendationResponse> {
  // Map frontend camelCase field names to backend snake_case field names.
  const requestBody = {
    listing_title: formData.listingTitle,
    city: formData.city,
    property_type: formData.propertyType,
    beds: Number(formData.beds),
    bathrooms: Number(formData.bathrooms),
    accommodates: Number(formData.accommodates),
    competitor_avg_price: 
      formData.competitorAvgPrice.trim() === ""
        ? null
        : Number(formData.competitorAvgPrice),
  };

  // Send a POST request to the backend recommendation endpoint.
  const response = await fetch(`${API_BASE_URL}/api/v1/recommendations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  // If the response is not successful, throw an error.
  if (!response.ok) {
    throw new Error("Recommendation request failed.");
  }

  // Convert the backend JSON response into JavaScript data.
  return response.json();
}


// Create a reusable function for retrieving saved recommendation history.
export async function getRecommendationHistory(): Promise<
  RecommendationHistoryRecord[]
> {
  // Send a GET request to the backend history endpoint.
  const response = await fetch(`${API_BASE_URL}/api/v1/recommendations`);

  // If the response is not successful, throw an error.
  if (!response.ok) {
    throw new Error("Recommendation history request failed.");
  }

  // Convert the backend JSON response into JavaScript data.
  return response.json();
}