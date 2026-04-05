"""
Service functions for pricing recommendation logic.

This file contains the business logic used to generate pricing
recommendations. Keeping this logic separate from the route file
makes the backend easier to maintain and extend.
"""

from sqlmodel import Session, select

from app.core.database import engine
from app.ml.inference import predict_price
from app.models.recommendation import Recommendation
from app.schemas.pricing import (
    PricingRequest,
    PricingResponse,
    RecommendationHistoryResponse,
)


def generate_model_recommendation(
    pricing_request: PricingRequest,
) -> PricingResponse:
    """
    Generate a model-based pricing recommendation and save it.

    Args:
        pricing_request (PricingRequest): The validated listing input data
        sent from the frontend.

    Returns:
        PricingResponse: A model-based recommendation and explanation.
    """
    recommended_price, market_price_used, used_fallback = predict_price(
        listing_title=pricing_request.listing_title,
        city=pricing_request.city,
        property_type=pricing_request.property_type,
        beds=pricing_request.beds,
        accommodates=pricing_request.accommodates,
        competitor_avg_price=pricing_request.competitor_avg_price,
    )

    if used_fallback:
        explanation = (
            "This recommendation is based on your listing's property type, city, "
            "bed count, accommodates value, and an estimated nearby market price "
            "generated from similar listings."
        )
    else:
        explanation = (
            "This recommendation is based on your listing's property type, city, "
            "bed count, accommodates value, and observed nearby market price."
        )

    saved_recommendation = Recommendation(
        listing_title=pricing_request.listing_title,
        city=pricing_request.city,
        property_type=pricing_request.property_type,
        beds=pricing_request.beds,
        bathrooms=pricing_request.bathrooms,
        accommodates=pricing_request.accommodates,
        competitor_avg_price=market_price_used,
        used_fallback_market_price=used_fallback,
        recommended_price=recommended_price,
        explanation=explanation,
    )

    with Session(engine) as session:
        session.add(saved_recommendation)
        session.commit()
        session.refresh(saved_recommendation)

    return PricingResponse(
        recommended_price=recommended_price,
        explanation=explanation,
    )


def get_saved_recommendations() -> list[RecommendationHistoryResponse]:
    """
    Retrieve all saved recommendation records from the database.

    Returns:
        list[RecommendationHistoryResponse]: A list of saved recommendation
        history records.
    """
    with Session(engine) as session:
        statement = select(Recommendation).order_by(Recommendation.id.desc())
        saved_recommendations = session.exec(statement).all()

    return [
        RecommendationHistoryResponse(
            id=recommendation.id,
            listing_title=recommendation.listing_title,
            city=recommendation.city,
            property_type=recommendation.property_type,
            beds=recommendation.beds,
            bathrooms=recommendation.bathrooms,
            accommodates=recommendation.accommodates,
            competitor_avg_price=recommendation.competitor_avg_price,
            used_fallback_market_price=recommendation.used_fallback_market_price,
            recommended_price=recommendation.recommended_price,
            explanation=recommendation.explanation,
        )
        for recommendation in saved_recommendations
    ]