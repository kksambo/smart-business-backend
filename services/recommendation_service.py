"""
AI-powered product recommendation service
Analyzes sales patterns by location and suggests complementary products
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from collections import Counter


class ComplementaryProductsAnalyzer:
    """
    Analyzes sales data to identify and recommend complementary products
    Uses frequency analysis and product co-occurrence patterns
    """
    
    # Predefined complementary product rules
    COMPLEMENTARY_RULES = {
        "Sugar": ["Tea", "Coffee", "Milk", "Honey"],
        "Tea": ["Sugar", "Coffee", "Milk", "Honey", "Cups"],
        "Coffee": ["Sugar", "Tea", "Milk", "Cups"],
        "Rice 5kg": ["Cooking Oil 2L", "Salt", "Beans", "Vegetables"],
        "Cooking Oil 2L": ["Rice 5kg", "Beans", "Salt", "Spices"],
        "Beans": ["Rice 5kg", "Cooking Oil 2L", "Salt", "Vegetables"],
        "A4 Paper Pack": ["Ballpoint Pens", "Notebooks", "Stapler", "File Folders"],
        "Ballpoint Pens": ["A4 Paper Pack", "Notebooks", "Correction Tape"],
        "Notebooks": ["Ballpoint Pens", "A4 Paper Pack", "Highlighters"],
        "T-Shirt": ["Jeans", "Sneakers", "Socks Pack", "Underwear"],
        "Jeans": ["T-Shirt", "Sneakers", "Belt", "Underwear"],
        "Sneakers": ["T-Shirt", "Jeans", "Socks Pack", "Shoe Cream"],
        "Dress": ["Accessories", "Shoes", "Scarf", "Sunglasses"],
        "Laptop": ["Mouse", "Keyboard", "USB Cable", "Laptop Stand"],
        "Smartphone": ["Phone Case", "Screen Protector", "USB Cable", "Charger"],
        "Mouse": ["Laptop", "Keyboard", "USB Cable", "Mousepad"],
        "Power Bank": ["USB Cable", "Smartphone", "Charger"],
    }

    @staticmethod
    def get_top_products_by_location(
        db: Session,
        location_id: int,
        owner_id: int,
        days: int = 30,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get top selling products for a location
        
        Args:
            db: Database session
            location_id: Location ID
            owner_id: Owner/User ID
            days: Number of days to analyze (default 30)
            limit: Maximum products to return
        
        Returns:
            List of top products with sales count
        """
        from models import Sale, SalesItem, Product
        
        date_threshold = datetime.now() - timedelta(days=days)
        
        query = db.query(
            Product.name,
            func.sum(SalesItem.quantity).label("total_quantity"),
            func.count(SalesItem.id).label("sale_count"),
            func.avg(SalesItem.unit_price).label("avg_price")
        ).join(
            SalesItem, Product.id == SalesItem.product_id
        ).join(
            Sale, SalesItem.sale_id == Sale.id
        ).filter(
            Sale.location_id == location_id,
            Sale.owner_id == owner_id,
            Sale.created_at >= date_threshold
        ).group_by(
            Product.name
        ).order_by(
            func.sum(SalesItem.quantity).desc()
        ).limit(limit).all()
        
        return [
            {
                "product_name": row[0],
                "total_quantity": row[1] or 0,
                "sale_count": row[2] or 0,
                "avg_price": float(row[3] or 0)
            }
            for row in query
        ]

    @staticmethod
    def get_product_pairs(
        db: Session,
        location_id: int,
        owner_id: int,
        days: int = 30,
        min_co_occurrence: int = 2
    ) -> Dict[str, int]:
        """
        Get products that are frequently purchased together
        
        Args:
            db: Database session
            location_id: Location ID
            owner_id: Owner ID
            days: Number of days to analyze
            min_co_occurrence: Minimum times two products must be bought together
        
        Returns:
            Dictionary of product pairs and their co-occurrence count
        """
        from models import Sale, SalesItem, Product
        
        date_threshold = datetime.now() - timedelta(days=days)
        
        # Get all sales in the period
        sales = db.query(Sale.id).filter(
            Sale.location_id == location_id,
            Sale.owner_id == owner_id,
            Sale.created_at >= date_threshold
        ).all()
        
        sale_ids = [s[0] for s in sales]
        
        if not sale_ids:
            return {}
        
        # Get all product pairs from the same sales
        product_pairs = Counter()
        
        for sale_id in sale_ids:
            products = db.query(Product.name).join(
                SalesItem, Product.id == SalesItem.product_id
            ).filter(
                SalesItem.sale_id == sale_id
            ).all()
            
            product_names = [p[0] for p in products]
            
            # Count pairs
            for i in range(len(product_names)):
                for j in range(i + 1, len(product_names)):
                    pair = tuple(sorted([product_names[i], product_names[j]]))
                    product_pairs[pair] += 1
        
        # Filter by minimum co-occurrence
        return {
            f"{p[0]} + {p[1]}": count
            for p, count in product_pairs.items()
            if count >= min_co_occurrence
        }

    @staticmethod
    def recommend_products(
        db: Session,
        location_id: int,
        owner_id: int,
        limit: int = 5,
        days: int = 30
    ) -> List[Dict]:
        """
        Generate product recommendations based on location sales patterns
        
        Args:
            db: Database session
            location_id: Location ID
            owner_id: Owner ID
            limit: Maximum recommendations
            days: Days to analyze
        
        Returns:
            List of recommended products with reasoning
        """
        from models import Sale, SalesItem, Product
        
        recommendations = []
        scored_products = {}
        
        # Get top products
        top_products = ComplementaryProductsAnalyzer.get_top_products_by_location(
            db, location_id, owner_id, days, limit
        )
        
        if not top_products:
            return []
        
        # For each top product, find complementary products
        for top_product in top_products:
            product_name = top_product["product_name"]
            
            # Check predefined rules
            if product_name in ComplementaryProductsAnalyzer.COMPLEMENTARY_RULES:
                complementary = ComplementaryProductsAnalyzer.COMPLEMENTARY_RULES[product_name]
                
                for comp_product in complementary:
                    if comp_product not in scored_products:
                        scored_products[comp_product] = {
                            "score": 0,
                            "reason": [],
                            "top_product": product_name
                        }
                    
                    scored_products[comp_product]["score"] += 10
                    scored_products[comp_product]["reason"].append(
                        f"Often bought with {product_name}"
                    )
        
        # Get actual product co-occurrence data
        product_pairs = ComplementaryProductsAnalyzer.get_product_pairs(
            db, location_id, owner_id, days
        )
        
        for pair_str, count in product_pairs.items():
            products = pair_str.split(" + ")
            
            # Add score for actual co-occurrence
            for p in products:
                if p not in scored_products:
                    scored_products[p] = {
                        "score": 0,
                        "reason": [],
                        "top_product": top_products[0]["product_name"] if top_products else ""
                    }
                scored_products[p]["score"] += min(count * 2, 20)
                other_product = products[1] if products[0] == p else products[0]
                scored_products[p]["reason"].append(
                    f"Frequently paired with {other_product} ({count} times)"
                )
        
        # Sort by score and create recommendations
        sorted_recommendations = sorted(
            scored_products.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )[:limit]
        
        for product_name, data in sorted_recommendations:
            recommendations.append({
                "product_name": product_name,
                "recommendation_score": data["score"],
                "reason": data["reason"][0] if data["reason"] else "Popular in this area",
                "top_product": data["top_product"],
                "confidence": min(data["score"] / 30, 1.0)  # Normalize to 0-1
            })
        
        return recommendations

    @staticmethod
    def get_location_insights(
        db: Session,
        location_id: int,
        owner_id: int,
        days: int = 30
    ) -> Dict:
        """
        Get comprehensive insights for a location
        
        Args:
            db: Database session
            location_id: Location ID
            owner_id: Owner ID
            days: Days to analyze
        
        Returns:
            Dictionary with location insights
        """
        from models import Sale, SalesItem
        
        date_threshold = datetime.now() - timedelta(days=days)
        
        # Get sales stats
        sales = db.query(Sale).filter(
            Sale.location_id == location_id,
            Sale.owner_id == owner_id,
            Sale.created_at >= date_threshold
        ).all()
        
        if not sales:
            return {
                "location_id": location_id,
                "total_sales": 0,
                "average_transaction": 0,
                "total_items_sold": 0,
                "unique_products": 0,
                "profit_margin": 0
            }
        
        total_sales = sum(s.total_amount for s in sales)
        total_cost = sum(s.total_cost for s in sales)
        total_profit = total_sales - total_cost
        num_sales = len(sales)
        
        # Get unique products
        items = db.query(SalesItem).filter(
            SalesItem.sale_id.in_([s.id for s in sales])
        ).all()
        
        total_items = sum(item.quantity for item in items)
        unique_products = len(set(item.product_id for item in items))
        
        return {
            "location_id": location_id,
            "total_sales": float(total_sales),
            "average_transaction": float(total_sales / num_sales) if num_sales > 0 else 0,
            "total_items_sold": total_items,
            "unique_products": unique_products,
            "profit_margin": float((total_profit / total_sales * 100) if total_sales > 0 else 0),
            "num_transactions": num_sales
        }
