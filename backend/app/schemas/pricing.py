"""
Schemas for pricing-related API requests and responses.

This file defines the data shape the backend expects for pricing
recommendation requests and the shape of the responses it returns.
"""

from typing import Optional

from pydantic import BaseModel


class PricingRequest(BaseModel):
    """
    Schema for incoming pricing recommendation requests.

    These fields represent the listing and market inputs sent
    from the React frontend to the FastAPI backend.
    """

    listing_title: str
    city: str
    property_type: str
    beds: int
    bathrooms: int
    accommodates: int
    competitor_avg_price: Optional[float] = None


class PricingResponse(BaseModel):
    """
    Schema for outgoing pricing recommendation responses.

    This is the response model used when a recommendation is
    generated and returned to the frontend.
    """

    recommended_price: float
    explanation: str


class RecommendationHistoryResponse(BaseModel):
    """
    Schema for a saved recommendation history record.

    This model is used when returning stored recommendation
    records from the database.
    """

    id: int
    listing_title: str
    city: str
    property_type: str
    beds: int
    bathrooms: int
    accommodates: int
    competitor_avg_price: float
    used_fallback_market_price: bool
    recommended_price: float
    explanation: str