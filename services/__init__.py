"""
Business logic services for analytics, ML predictions, and AI insights
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta, date
from typing import List, Dict, Tuple, Any
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from models import (
    User, Product, Sale, SalesItem, Customer, Location,
    Analytics, Prediction, BusinessInsight, BusinessLocation
)
from schemas import PredictionResponse, BusinessInsightResponse


class AnalyticsService:
    """Service for calculating business analytics"""

    @staticmethod
    def get_daily_analytics(db: Session, user_id: int, target_date: date) -> Dict[str, Any]:
        """Calculate daily analytics for a specific user"""
        sales = db.query(Sale).filter(
            and_(
                Sale.owner_id == user_id,
                func.date(Sale.created_at) == target_date
            )
        ).all()

        if not sales:
            return {
                "total_sales": 0,
                "total_profit": 0,
                "transaction_count": 0,
                "average_transaction": 0,
            }

        total_sales = sum(sale.total_amount for sale in sales)
        total_profit = sum(sale.profit for sale in sales)

        return {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "transaction_count": len(sales),
            "average_transaction": total_sales / len(sales) if sales else 0,
        }

    @staticmethod
    def get_period_analytics(db: Session, user_id: int, start_date: date, end_date: date) -> Dict[str, Any]:
        """Calculate analytics for a period"""
        sales = db.query(Sale).filter(
            and_(
                Sale.owner_id == user_id,
                func.date(Sale.created_at) >= start_date,
                func.date(Sale.created_at) <= end_date
            )
        ).all()

        if not sales:
            return {
                "total_sales": 0,
                "total_profit": 0,
                "transaction_count": 0,
                "average_transaction": 0,
            }

        total_sales = sum(sale.total_amount for sale in sales)
        total_profit = sum(sale.profit for sale in sales)
        total_cost = sum(sale.total_cost for sale in sales)

        return {
            "total_sales": total_sales,
            "total_profit": total_profit,
            "total_cost": total_cost,
            "transaction_count": len(sales),
            "average_transaction": total_sales / len(sales) if sales else 0,
            "profit_margin": (total_profit / total_sales * 100) if total_sales > 0 else 0,
        }

    @staticmethod
    def get_top_products(db: Session, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top-selling products"""
        results = db.query(
            Product.id,
            Product.name,
            func.sum(SalesItem.quantity).label("total_quantity"),
            func.sum(SalesItem.subtotal).label("total_revenue"),
            func.count(SalesItem.id).label("times_sold")
        ).join(SalesItem).join(Sale).filter(
            and_(
                Sale.owner_id == user_id,
                Product.is_active == True
            )
        ).group_by(Product.id, Product.name).order_by(
            desc(func.sum(SalesItem.subtotal))
        ).limit(limit).all()

        return [
            {
                "product_id": r[0],
                "name": r[1],
                "quantity_sold": r[2] or 0,
                "revenue": r[3] or 0,
                "times_sold": r[4] or 0,
            }
            for r in results
        ]

    @staticmethod
    def get_worst_products(db: Session, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get worst-selling products"""
        results = db.query(
            Product.id,
            Product.name,
            func.coalesce(func.sum(SalesItem.quantity), 0).label("total_quantity"),
            func.coalesce(func.sum(SalesItem.subtotal), 0).label("total_revenue"),
            func.coalesce(func.count(SalesItem.id), 0).label("times_sold")
        ).join(
            SalesItem,
            Product.id == SalesItem.product_id,
            isouter=True
        ).join(
            Sale,
            SalesItem.sale,
            isouter=True
        ).filter(
            and_(
                Product.owner_id == user_id,
                Product.is_active == True
            )
        ).group_by(Product.id, Product.name).order_by(
            func.coalesce(func.sum(SalesItem.subtotal), 0).asc()
        ).limit(limit).all()

        return [
            {
                "product_id": r[0],
                "name": r[1],
                "quantity_sold": r[2] or 0,
                "revenue": r[3] or 0,
                "times_sold": r[4] or 0,
            }
            for r in results
        ]

    @staticmethod
    def get_dashboard_metrics(db: Session, user_id: int) -> Dict[str, Any]:
        """Get comprehensive dashboard metrics"""
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # Daily metrics
        daily_metrics = AnalyticsService.get_period_analytics(db, user_id, today, today)

        # Weekly metrics
        weekly_metrics = AnalyticsService.get_period_analytics(db, user_id, week_ago, today)

        # Monthly metrics
        monthly_metrics = AnalyticsService.get_period_analytics(db, user_id, month_ago, today)

        # Product metrics
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}

        total_products = db.query(func.count(Product.id)).filter(
            and_(Product.owner_id == user_id, Product.is_active == True)
        ).scalar() or 0

        low_stock_products = db.query(func.count(Product.id)).filter(
            and_(
                Product.owner_id == user_id,
                Product.quantity <= 10,
                Product.is_active == True
            )
        ).scalar() or 0

        return {
            "daily": daily_metrics,
            "weekly": weekly_metrics,
            "monthly": monthly_metrics,
            "total_products": total_products,
            "low_stock_products": low_stock_products,
            "top_products": AnalyticsService.get_top_products(db, user_id, 5),
            "worst_products": AnalyticsService.get_worst_products(db, user_id, 5),
        }

    @staticmethod
    def get_public_business_summaries(
        db: Session,
        category: str = None,
        min_revenue: float = None,
        max_revenue: float = None,
        region: str = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Return summary data for public market map exploration."""
        query = db.query(BusinessLocation)

        if region:
            query = query.filter(BusinessLocation.region == region)

        businesses = query.order_by(BusinessLocation.total_sales.desc()).limit(limit).all()

        public_data = []
        for location in businesses:
            top_products = []
            categories = []

            category_rows = db.query(Product.category).join(SalesItem).join(Sale).filter(
                and_(Sale.owner_id == location.owner_id, Product.owner_id == location.owner_id)
            ).distinct().all()
            categories = [row[0] for row in category_rows if row[0]]

            top_query = db.query(
                Product.name,
                func.sum(SalesItem.subtotal).label("revenue")
            ).join(SalesItem).join(Sale).filter(
                and_(
                    Sale.owner_id == location.owner_id,
                    Product.owner_id == location.owner_id
                )
            ).group_by(Product.name).order_by(desc(func.sum(SalesItem.subtotal))).limit(3).all()

            for row in top_query:
                _, revenue = row
                top_products.append({
                    "name": row[0],
                    "revenue": float(revenue or 0),
                })

            performance = "low"
            if location.total_sales >= 20000:
                performance = "high"
            elif location.total_sales >= 8000:
                performance = "medium"

            public_data.append({
                "id": location.id,
                "name": location.name,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "formatted_address": location.formatted_address,
                "city": location.city,
                "province_state": location.province_state,
                "region": location.region,
                "total_sales": float(location.total_sales or 0),
                "product_categories": categories,
                "top_products": top_products,
                "sales_performance": performance,
                "business_owner": location.owner.business_name if location.owner else None,
            })

        if min_revenue is not None:
            public_data = [item for item in public_data if item["total_sales"] >= min_revenue]
        if max_revenue is not None:
            public_data = [item for item in public_data if item["total_sales"] <= max_revenue]
        if category:
            public_data = [item for item in public_data if category in item["product_categories"]]

        return public_data

    @staticmethod
    def get_area_heatmap(db: Session) -> List[Dict[str, Any]]:
        """Build heatmap metadata for public map analytics."""
        results = db.query(
            BusinessLocation.latitude,
            BusinessLocation.longitude,
            BusinessLocation.region,
            BusinessLocation.total_sales,
        ).all()

        return [
            {
                "latitude": row[0],
                "longitude": row[1],
                "region": row[2],
                "intensity": float((row[3] or 0) / 10000),
            }
            for row in results
        ]

    @staticmethod
    def get_trending_products(db: Session, limit: int = 8) -> List[Dict[str, Any]]:
        """Return top product trends across the platform."""
        results = db.query(
            Product.category,
            func.sum(SalesItem.subtotal).label("revenue"),
            func.sum(SalesItem.quantity).label("quantity")
        ).join(SalesItem).join(Sale).group_by(Product.category).order_by(desc(func.sum(SalesItem.subtotal))).limit(limit).all()

        return [
            {
                "category": row[0] or "Unknown",
                "revenue": float(row[1] or 0),
                "quantity": int(row[2] or 0),
                "demand_score": float(min(100, ((row[1] or 0) / 1000) * 10)),
            }
            for row in results
        ]

    @staticmethod
    def get_public_opportunities(db: Session) -> List[Dict[str, Any]]:
        """Return AI-style opportunity summaries for the public market page."""
        categories = AnalyticsService.get_trending_products(db, limit=5)
        regions = db.query(
            BusinessLocation.region,
            func.sum(BusinessLocation.total_sales).label("region_sales")
        ).group_by(BusinessLocation.region).order_by(desc(func.sum(BusinessLocation.total_sales))).limit(4).all()

        top_regions = [row[0] for row in regions if row[0]]

        insights = []
        if categories:
            insights.append({
                "title": "Fast-moving categories in demand",
                "description": f"{categories[0]['category']} and {categories[1]['category']} are showing strong revenue momentum across popular regions.",
                "details": categories,
            })

        if top_regions:
            insights.append({
                "title": "High activity areas",
                "description": f"Business activity is strongest in {', '.join(top_regions[:3])}. Consider locating complementary services there.",
                "details": [{"region": region, "score": float(min(100, (idx + 1) * 20))} for idx, region in enumerate(top_regions[:3])],
            })

        return insights


class MLPredictionService:
    """Machine learning prediction service"""

    @staticmethod
    def prepare_sales_data(db: Session, user_id: int, days: int = 90) -> Tuple[List[float], List[float]]:
        """Prepare historical sales data for ML training"""
        start_date = date.today() - timedelta(days=days)

        daily_data = []
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            analytics = AnalyticsService.get_daily_analytics(db, user_id, current_date)
            daily_data.append(analytics["total_sales"])

        # Create time series
        X = np.array(range(len(daily_data))).reshape(-1, 1)
        y = np.array(daily_data)

        return X, y

    @staticmethod
    def predict_daily_sales(db: Session, user_id: int, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """Predict sales for the next N days"""
        try:
            X, y = MLPredictionService.prepare_sales_data(db, user_id)

            if len(X) < 5:
                return []

            model = LinearRegression()
            model.fit(X, y)

            predictions = []
            for i in range(days_ahead):
                next_day = len(X) + i
                predicted_value = max(0, model.predict([[next_day]])[0])

                # Calculate confidence based on variance
                predictions_scatter = model.predict(X)
                residuals = y - predictions_scatter
                std_dev = np.std(residuals)
                confidence = max(0, min(1, 1 - (std_dev / (np.mean(y) + 1))))

                predictions.append({
                    "day": i + 1,
                    "predicted_sales": float(predicted_value),
                    "confidence": float(confidence),
                })

            return predictions
        except Exception as e:
            print(f"Error in sales prediction: {e}")
            return []

    @staticmethod
    def predict_product_demand(db: Session, user_id: int, product_id: int) -> Dict[str, Any]:
        """Predict demand for a specific product"""
        try:
            # Get product sales history
            sales_items = db.query(SalesItem).join(Sale).filter(
                and_(
                    Sale.owner_id == user_id,
                    SalesItem.product_id == product_id
                )
            ).all()

            if len(sales_items) < 3:
                return {
                    "predicted_quantity": 0,
                    "confidence": 0,
                    "recommendation": "Insufficient sales history",
                }

            quantities = [item.quantity for item in sales_items]
            X = np.array(range(len(quantities))).reshape(-1, 1)
            y = np.array(quantities)

            model = LinearRegression()
            model.fit(X, y)

            # Predict next period
            next_period = len(X)
            predicted_quantity = max(1, int(model.predict([[next_period]])[0]))

            predictions_scatter = model.predict(X)
            residuals = y - predictions_scatter
            std_dev = np.std(residuals)
            confidence = max(0, min(1, 1 - (std_dev / (np.mean(y) + 1))))

            return {
                "predicted_quantity": predicted_quantity,
                "confidence": float(confidence),
                "recommendation": f"Recommend restocking {predicted_quantity} units",
            }
        except Exception as e:
            return {"predicted_quantity": 0, "confidence": 0, "error": str(e)}

    @staticmethod
    def predict_profit_margin(db: Session, user_id: int) -> Dict[str, Any]:
        """Predict future profit margins"""
        try:
            analytics_records = db.query(Analytics).filter(
                Analytics.owner_id == user_id
            ).order_by(Analytics.date.desc()).limit(30).all()

            if len(analytics_records) < 3:
                return {"predicted_margin": 0, "confidence": 0}

            profit_margins = []
            for record in reversed(analytics_records):
                if record.total_revenue > 0:
                    margin = (record.total_profit / record.total_revenue) * 100
                    profit_margins.append(margin)

            if not profit_margins:
                return {"predicted_margin": 0, "confidence": 0}

            X = np.array(range(len(profit_margins))).reshape(-1, 1)
            y = np.array(profit_margins)

            model = LinearRegression()
            model.fit(X, y)

            next_period = len(X)
            predicted_margin = max(0, model.predict([[next_period]])[0])

            predictions_scatter = model.predict(X)
            residuals = y - predictions_scatter
            std_dev = np.std(residuals)
            confidence = max(0, min(1, (100 - std_dev) / 100))

            return {
                "predicted_margin": float(predicted_margin),
                "confidence": float(confidence),
            }
        except Exception as e:
            return {"predicted_margin": 0, "confidence": 0, "error": str(e)}


class InsightService:
    """Service for generating AI business insights using Groq"""

    @staticmethod
    # Load .env variables


    def get_groq_client():
        return Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    @staticmethod
    def generate_ai_recommendations(
        top_products: List[Dict[str, Any]],
        worst_products: List[Dict[str, Any]],
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        try:
            client = InsightService.get_groq_client()

            prompt = f"""
            You are a smart retail business analyst AI.

            Analyze the business data below and generate business insights focused on location, customer demand, product mix, and sales performance.

            TOP PRODUCTS:
            {json.dumps(top_products, indent=2)}

            WORST PRODUCTS:
            {json.dumps(worst_products, indent=2)}

            BUSINESS METRICS:
            {json.dumps(metrics, indent=2)}

            Use geographic and sales performance signals to suggest:
            - the best opportunities by area and category
            - local demand and product mix recommendations
            - store location improvements
            - promotional strategies for high-opportunity zones
            - inventory recommendations for likely demand spikes

            Return ONLY valid JSON array in this exact format:

            [
              {{
                "insight_type": "sales",
                "title": "Top Performer: Jacket",
                "description": "Jacket is selling extremely well.",
                "recommendation": "Bundle jackets with caps and sneakers.",
                "impact_potential": "high"
              }}
            ]

            Do not return explanations.
            """

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1200,
            )

            content = response.choices[0].message.content

            # Clean markdown if returned
            content = content.replace("```json", "").replace("```", "").strip()

            insights = json.loads(content)

            return insights

        except Exception as e:
            print("Groq Error:", e)

            return [
                {
                    "insight_type": "sales",
                    "title": "Business Growth Suggestion",
                    "description": "AI could not generate advanced insights.",
                    "recommendation": "Focus on promoting best-selling products and improving customer retention.",
                    "impact_potential": "medium"
                }
            ]

    @staticmethod
    def generate_insights(db: Session, user_id: int) -> None:
        """Generate AI insights"""

        # Remove old insights
        db.query(BusinessInsight).filter(
            BusinessInsight.owner_id == user_id
        ).delete()

        top_products = AnalyticsService.get_top_products(db, user_id, 5)

        worst_products = AnalyticsService.get_worst_products(db, user_id, 5)

        metrics = AnalyticsService.get_dashboard_metrics(db, user_id)

        ai_insights = InsightService.generate_ai_recommendations(
            top_products,
            worst_products,
            metrics
        )

        for item in ai_insights:

            insight = BusinessInsight(
                owner_id=user_id,
                insight_type=item.get("insight_type", "sales"),
                title=item.get("title", "Business Insight"),
                description=item.get("description", ""),
                recommendation=item.get("recommendation", ""),
                impact_potential=item.get("impact_potential", "medium"),
                is_read=False,
            )

            db.add(insight)

        # Low stock alerts
        low_stock_products = db.query(Product).filter(
            and_(
                Product.owner_id == user_id,
                Product.quantity <= 10,
                Product.is_active == True
            )
        ).all()

        for product in low_stock_products:

            insight = BusinessInsight(
                owner_id=user_id,
                insight_type="inventory",
                title=f"Low Stock Alert: {product.name}",
                description=f"'{product.name}' only has {product.quantity} units remaining.",
                recommendation=f"Restock '{product.name}' soon to avoid losing sales.",
                impact_potential="high",
                is_read=False,
            )

            db.add(insight)

        db.commit()

    @staticmethod
    def get_recent_insights(
        db: Session,
        user_id: int,
        limit: int = 10
    ) -> List[BusinessInsight]:

        return db.query(BusinessInsight).filter(
            BusinessInsight.owner_id == user_id
        ).order_by(
            BusinessInsight.created_at.desc()
        ).limit(limit).all()