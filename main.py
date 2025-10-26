from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os

from core.queryhandler import process_query, validate_user_input
from core.scraper import scrape_pinterest, get_trending_styles
from core.recommender import (
    recommend_outfits, create_outfit_combinations, get_recommendation_summary
)
from core.feedback import (
    record_feedback, get_user_feedback, get_trending_items, analyze_feedback_trends
)
from core.analyzer import generate_personalized_explanation
from core.storage import load_json, save_json, log_activity
from core.analyzer import generate_pinterest_recommendations

# IMPORTANT: do NOT call external APIs at import time.
# (Deleted the top-level print(...) that called Gemini here.)

app = FastAPI(
    title="FitFindr API",
    description="AI-powered fashion recommendation system",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to FitFindr API",
        "version": "1.0.0",
        "endpoints": {
            "query": "/query - Process user style and image",
            "scrape": "/scrape - Scrape Pinterest for items",
            "recommend": "/recommend - Get outfit recommendations",
            "feedback": "/feedback - Record user feedback",
            "analyze": "/analyze - Get AI analysis",
            "trending": "/trending - Get trending items",
            "styles": "/styles - Get available styles"
        }
    }

@app.post("/query")
async def query_user(style: str = Form(...), image: Optional[UploadFile] = File(None)):
    try:
        image_data = None
        if image:
            image_data = await image.read()
            is_valid, error = validate_user_input(style, image_data, image.filename)
        else:
            is_valid, error = validate_user_input(style)

        if not is_valid:
            raise HTTPException(status_code=400, detail=error)

        user_data = await process_query(style, image_data)

        users = load_json("users.json", [])
        users.append(user_data)
        save_json("users.json", users)

        log_activity("user_query_processed", {
            "user_id": user_data["id"],
            "style": style,
            "has_image": image_data is not None
        })
        return {"message": "Query processed successfully", "user": user_data, "status": "success"}

    except Exception as e:
        log_activity("query_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/scrape")
async def scrape_items_route(payload: dict):
    """Scrape Pinterest (via Gemini) for fashion items."""
    try:
        keyword = payload.get("keyword", "vintage streetwear")
        max_items = payload.get("max_items", 20)
        log_activity("scrape_requested", {"keyword": keyword, "max_items": max_items})

        items = generate_pinterest_recommendations(keyword, max_items) or []
        # If Gemini returns None or an unexpected shape, we fall back to an empty list instead of crashing.

        save_json("items.json", items)
        return {"message": "Items scraped successfully", "count": len(items), "items": items, "keyword": keyword}

    except Exception as e:
        log_activity("scrape_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error scraping items: {str(e)}")

@app.post("/recommend")
async def recommend_route(payload: dict = None):
    try:
        users = load_json("users.json", [])
        if not users:
            raise HTTPException(status_code=400, detail="No user data found. Please process a query first.")

        user = users[-1]
        items = load_json("items.json", [])
        if not items:
            raise HTTPException(status_code=400, detail="No items found. Please scrape items first.")

        max_recommendations = payload.get("max_recommendations", 10) if payload else 10
        recommendations = recommend_outfits(user, items, max_recommendations)
        outfits = create_outfit_combinations(recommendations)
        summary = get_recommendation_summary(recommendations)
        save_json("recommendations.json", recommendations)

        log_activity("recommendations_generated", {
            "user_id": user["id"],
            "recommendation_count": len(recommendations),
            "outfit_count": len(outfits)
        })

        return {
            "message": "Recommendations generated successfully",
            "user": user,
            "recommendations": recommendations,
            "outfits": outfits,
            "summary": summary
        }

    except Exception as e:
        log_activity("recommendation_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/feedback")
async def feedback_route(payload: dict):
    try:
        for field in ["user_id", "item_id", "feedback_type"]:
            if field not in payload:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        fb = record_feedback(payload)
        log_activity("feedback_recorded", {
            "user_id": payload["user_id"],
            "item_id": payload["item_id"],
            "feedback_type": payload["feedback_type"]
        })
        return {"message": "Feedback recorded successfully", "feedback": fb}

    except Exception as e:
        log_activity("feedback_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error recording feedback: {str(e)}")

@app.post("/analyze")
async def analyze_route(payload: dict):
    try:
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        users = load_json("users.json", [])
        user = next((u for u in users if u.get("id") == user_id), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        recommendations = load_json("recommendations.json", [])
        user_recs = [r for r in recommendations if r.get("user_id") == user_id] or recommendations[:5]

        explanation = generate_personalized_explanation(user, user_recs)

        return {
            "message": "Analysis completed successfully",
            "user_profile": user,
            "personalized_explanation": explanation,
            "recommendation_count": len(user_recs)
        }

    except Exception as e:
        log_activity("analysis_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error in analysis: {str(e)}")

@app.get("/trending")
async def trending_route():
    try:
        trending_items = get_trending_items(10)
        return {"message": "Trending items retrieved successfully", "trending_items": trending_items, "count": len(trending_items)}
    except Exception as e:
        log_activity("trending_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error getting trending items: {str(e)}")

@app.get("/styles")
async def styles_route():
    try:
        styles = get_trending_styles()
        return {"message": "Available styles retrieved successfully", "styles": styles, "count": len(styles)}
    except Exception as e:
        log_activity("styles_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error getting styles: {str(e)}")

@app.get("/user/{user_id}/feedback")
async def get_user_feedback_route(user_id: str):
    try:
        feedback_summary = get_user_feedback(user_id)
        return {"message": "User feedback retrieved successfully", "user_id": user_id, "feedback_summary": feedback_summary}
    except Exception as e:
        log_activity("user_feedback_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error getting user feedback: {str(e)}")

@app.get("/analytics")
async def analytics_route():
    try:
        analytics = analyze_feedback_trends()
        return {"message": "Analytics retrieved successfully", "analytics": analytics}
    except Exception as e:
        log_activity("analytics_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
