import { useState } from "react";
import {
  createRecommendation,
  type PricingFormData,
  type RecommendationResponse,
} from "../api/client";


// Define the props expected by the PricingForm component.
type PricingFormProps = {
  onRecommendationCreated: () => void;
};


// Define the shape of form validation errors.
type PricingFormErrors = {
  listingTitle?: string;
  city?: string;
  propertyType?: string;
  beds?: string;
  bathrooms?: string;
  accommodates?: string;
  competitorAvgPrice?: string;
};


// Standardized property type options for the project.
const PROPERTY_TYPE_OPTIONS = [
  { value: "house", label: "House" },
  { value: "apartment", label: "Apartment" },
  { value: "cabin", label: "Cabin" },
  { value: "condo", label: "Condo" },
  { value: "room", label: "Room" },
  { value: "villa", label: "Villa" },
  { value: "tiny_home", label: "Tiny Home" },
  { value: "treehouse", label: "Treehouse" },
  { value: "cottage", label: "Cottage" },
  { value: "guesthouse", label: "Guesthouse" },
  { value: "hotel", label: "Hotel" },
  { value: "loft", label: "Loft" },
  { value: "farm_stay", label: "Farm Stay" },
  { value: "guest_suite", label: "Guest Suite" },
  { value: "bungalow", label: "Bungalow" },
  { value: "chalet", label: "Chalet" },
  { value: "unique_stay", label: "Unique Stay" },
  { value: "other", label: "Other" },
];


// This component renders the host pricing input form.
function PricingForm({ onRecommendationCreated }: PricingFormProps) {
  // Store all form field values in a single piece of React state.
  const [formData, setFormData] = useState<PricingFormData>({
    listingTitle: "",
    city: "",
    propertyType: "",
    beds: "1",
    bathrooms: "1",
    accommodates: "1",
    competitorAvgPrice: "",
  });

  // Store validation error messages for individual fields.
  const [errors, setErrors] = useState<PricingFormErrors>({});

  // Store the returned recommendation so we can display it.
  const [recommendation, setRecommendation] =
    useState<RecommendationResponse | null>(null);

  // Store any error message separately so we can show it in the UI.
  const [errorMessage, setErrorMessage] = useState("");

  // Track whether the recommendation request is currently running.
  const [isLoading, setIsLoading] = useState(false);

  // Generic input change handler for all form fields.
  // Numeric-looking values stay as strings while the user is typing.
  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));

    // Clear the field-specific error once the user edits that field.
    setErrors((previousErrors) => ({
      ...previousErrors,
      [name]: undefined,
    }));
  };

  // Validate the form before sending data to the backend.
  const validateForm = (): PricingFormErrors => {
    const newErrors: PricingFormErrors = {};

    if (!formData.listingTitle.trim()) {
      newErrors.listingTitle = "Listing title is required.";
    }

    if (!formData.city.trim()) {
      newErrors.city = "City is required.";
    }

    if (!formData.propertyType) {
      newErrors.propertyType = "Property type is required.";
    }

    if (!formData.beds.trim() || Number(formData.beds) <= 0) {
      newErrors.beds = "Beds must be greater than 0.";
    }

    if (!formData.bathrooms.trim() || Number(formData.bathrooms) <= 0) {
      newErrors.bathrooms = "Bathrooms must be greater than 0.";
    }

    if (!formData.accommodates.trim() || Number(formData.accommodates) <= 0) {
      newErrors.accommodates = "Accommodates must be greater than 0.";
    }

    if (
  formData.competitorAvgPrice.trim() !== "" &&
  Number(formData.competitorAvgPrice) <= 0
) {
  newErrors.competitorAvgPrice =
    "Observed market price must be greater than 0 if provided.";
}

    return newErrors;
  };

  // Submit the form data to the backend recommendation endpoint.
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Run validation before sending the request.
    const validationErrors = validateForm();
    setErrors(validationErrors);

    // If any validation errors exist, stop submission.
    if (Object.keys(validationErrors).length > 0) {
      setRecommendation(null);
      return;
    }

    setRecommendation(null);
    setErrorMessage("");
    setIsLoading(true);

    try {
      const result = await createRecommendation(formData);
      setRecommendation(result);

      // Notify the parent component that a new recommendation
      // was created successfully so history can refresh.
      onRecommendationCreated();
    } catch (error) {
      setErrorMessage("Could not load a recommendation.");
      console.error("Recommendation error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h2>Host Pricing Input</h2>

        <div>
          <label htmlFor="listingTitle">Listing Title</label>
          <br />
          <input
            id="listingTitle"
            name="listingTitle"
            type="text"
            value={formData.listingTitle}
            onChange={handleChange}
          />
          {errors.listingTitle && <p>{errors.listingTitle}</p>}
        </div>

        <br />

        <div>
          <label htmlFor="city">City</label>
          <br />
          <input
            id="city"
            name="city"
            type="text"
            value={formData.city}
            onChange={handleChange}
          />
          {errors.city && <p>{errors.city}</p>}
        </div>

        <br />

        <div>
          <label htmlFor="propertyType">Property Type</label>
          <br />
          <select
            id="propertyType"
            name="propertyType"
            value={formData.propertyType}
            onChange={handleChange}
          >
            <option value="">Select a property type</option>
            {PROPERTY_TYPE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {errors.propertyType && <p>{errors.propertyType}</p>}
        </div>

        <br />

        <div>
          <label htmlFor="beds">Beds</label>
          <br />
          <input
            id="beds"
            name="beds"
            type="number"
            value={formData.beds}
            onChange={handleChange}
          />
          {errors.beds && <p>{errors.beds}</p>}
        </div>

        <br />

        <div>
          <label htmlFor="bathrooms">Bathrooms</label>
          <br />
          <input
            id="bathrooms"
            name="bathrooms"
            type="number"
            value={formData.bathrooms}
            onChange={handleChange}
          />
          {errors.bathrooms && <p>{errors.bathrooms}</p>}
        </div>

        <br />

        <div>
          <label htmlFor="accommodates">Accommodates</label>
          <br />
          <input
            id="accommodates"
            name="accommodates"
            type="number"
            value={formData.accommodates}
            onChange={handleChange}
          />
          {errors.accommodates && <p>{errors.accommodates}</p>}
        </div>

        <br />

        <div>
          <label htmlFor="competitorAvgPrice">Observed Market Price</label>
          <br />
          <p>(Enter the nightly price you found for similar nearby listings.)</p>
          <input
            id="competitorAvgPrice"
            name="competitorAvgPrice"
            type="number"
            value={formData.competitorAvgPrice}
            onChange={handleChange}
          />
          {errors.competitorAvgPrice && <p>{errors.competitorAvgPrice}</p>}
        </div>

        <br />

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Loading recommendation..." : "Get Recommendation"}
        </button>
      </form>

      <br />

      {recommendation && (
        <div>
          <h3>Recommendation Result</h3>
          <p>Recommended Price: ${recommendation.recommended_price}</p>
          <p>{recommendation.explanation}</p>
        </div>
      )}

      {errorMessage && <p>{errorMessage}</p>}
    </div>
  );
}


export default PricingForm;