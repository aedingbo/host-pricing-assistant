"""
Routes for pricing-related API endpoints.

This file defines pricing-related routes for creating
recommendations and retrieving saved recommendation history.
"""

from fastapi import APIRouter

from app.schemas.pricing import (
    PricingRequest,
    PricingResponse,
    RecommendationHistoryResponse,
)
from app.services.pricing_service import (
    generate_model_recommendation,
    get_saved_recommendations,
)


# Create a router object to group pricing-related endpoints together.
router = APIRouter(prefix="/api/v1", tags=["pricing"])


@router.post("/recommendations", response_model=PricingResponse)
def create_recommendation(pricing_request: PricingRequest):
    """
    Create a model-based pricing recommendation.

    Args:
        pricing_request (PricingRequest): The validated listing input data
        sent from the frontend.

    Returns:
        PricingResponse: A model-based recommendation and explanation.
    """
    return generate_model_recommendation(pricing_request)


@router.get("/recommendations", response_model=list[RecommendationHistoryResponse])
def read_recommendations():
    """
    Retrieve all saved pricing recommendations.

    Returns:
        list[RecommendationHistoryResponse]: Saved recommendation history.
    """
    return get_saved_recommendations()