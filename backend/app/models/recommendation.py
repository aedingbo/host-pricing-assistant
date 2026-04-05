"""
Database model for saved pricing recommendations.

This file defines the Recommendation table structure used to store
pricing request inputs and generated recommendation results.
"""

from typing import Optional

from sqlmodel import Field, SQLModel


class Recommendation(SQLModel, table=True):
    """
    Database model for a saved pricing recommendation.

    Each row represents one recommendation request and its resulting
    recommendation output.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    listing_title: str
    city: str
    property_type: str
    beds: int
    bathrooms: int
    accommodates: int
    competitor_avg_price: float
    used_fallback_market_price: bool = Field(default=False)
    recommended_price: float
    explanation: str