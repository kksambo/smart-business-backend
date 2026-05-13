"""
Receipt and recommendation API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from io import BytesIO
from datetime import datetime
from typing import Optional

from database import get_db
from models import Sale, SalesItem, Product, User, Location, Customer
from services.receipt_service import ReceiptService
from services.recommendation_service import ComplementaryProductsAnalyzer


router = APIRouter(prefix="/api", tags=["receipts", "recommendations"])


@router.get("/sales/{sale_id}/receipt/text")
def get_text_receipt(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """Get sale receipt in text format"""
    try:
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        
        # Get sale items
        items = db.query(SalesItem).filter(SalesItem.sale_id == sale_id).all()
        if not items:
            raise HTTPException(status_code=404, detail="No items found for this sale")
        
        # Get user and location info
        user = db.query(User).filter(User.id == sale.owner_id).first()
        location = db.query(Location).filter(Location.id == sale.location_id).first()
        customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
        
        # Prepare sale data
        sale_data = {
            "total_amount": sale.total_amount,
            "total_cost": sale.total_cost,
            "payment_method": sale.payment_method,
            "created_at": sale.created_at.isoformat(),
            "customer_name": customer.name if customer else "Walk-in Customer"
        }
        
        # Prepare business info
        business_info = {
            "business_name": user.business_name if user else "Smart Business",
            "business_type": user.business_type if user else "General"
        }
        
        # Prepare location info
        location_info = {
            "name": location.name if location else "",
            "region": location.region if location else ""
        } if location else None
        
        # Prepare items
        items_data = []
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            items_data.append({
                "product_name": product.name if product else "Item",
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "subtotal": float(item.subtotal)
            })
        
        # Generate receipt
        receipt_text = ReceiptService.generate_text_receipt(
            sale_data, business_info, items_data, location_info
        )
        
        return {
            "receipt": receipt_text,
            "format": "text",
            "sale_id": sale_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sales/{sale_id}/receipt/pdf")
def get_pdf_receipt(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """Get sale receipt as PDF file"""
    try:
        sale = db.query(Sale).filter(Sale.id == sale_id).first()
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        
        # Get sale items
        items = db.query(SalesItem).filter(SalesItem.sale_id == sale_id).all()
        if not items:
            raise HTTPException(status_code=404, detail="No items found for this sale")
        
        # Get user and location info
        user = db.query(User).filter(User.id == sale.owner_id).first()
        location = db.query(Location).filter(Location.id == sale.location_id).first()
        customer = db.query(Customer).filter(Customer.id == sale.customer_id).first()
        
        # Prepare sale data
        sale_data = {
            "total_amount": sale.total_amount,
            "total_cost": sale.total_cost,
            "payment_method": sale.payment_method,
            "created_at": sale.created_at.isoformat(),
            "customer_name": customer.name if customer else "Walk-in Customer"
        }
        
        # Prepare business info
        business_info = {
            "business_name": user.business_name if user else "Smart Business",
            "business_type": user.business_type if user else "General"
        }
        
        # Prepare location info
        location_info = {
            "name": location.name if location else "",
            "region": location.region if location else ""
        } if location else None
        
        # Prepare items
        items_data = []
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            items_data.append({
                "product_name": product.name if product else "Item",
                "quantity": item.quantity,
                "unit_price": float(item.unit_price),
                "subtotal": float(item.subtotal)
            })
        
        # Generate PDF
        pdf_bytes = ReceiptService.generate_pdf_receipt(
            sale_data, business_info, items_data, location_info
        )
        
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=receipt_{sale_id}.pdf"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/{location_id}/recommendations")
def get_location_recommendations(
    location_id: int,
    user_id: Optional[int] = Query(None),
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get AI-powered product recommendations for a location"""
    try:
        # Verify location exists
        location = db.query(Location).filter(Location.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        owner_id = user_id or location.owner_id
        
        # Get recommendations
        recommendations = ComplementaryProductsAnalyzer.recommend_products(
            db, location_id, owner_id, limit, days
        )
        
        # Get location insights
        insights = ComplementaryProductsAnalyzer.get_location_insights(
            db, location_id, owner_id, days
        )
        
        return {
            "location_id": location_id,
            "recommendations": recommendations,
            "insights": insights,
            "days_analyzed": days
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/{location_id}/top-products")
def get_location_top_products(
    location_id: int,
    user_id: Optional[int] = Query(None),
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get top selling products for a location"""
    try:
        location = db.query(Location).filter(Location.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        owner_id = user_id or location.owner_id
        
        top_products = ComplementaryProductsAnalyzer.get_top_products_by_location(
            db, location_id, owner_id, days, limit
        )
        
        return {
            "location_id": location_id,
            "top_products": top_products,
            "days_analyzed": days
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/locations/{location_id}/insights")
def get_location_insights(
    location_id: int,
    user_id: Optional[int] = Query(None),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get comprehensive insights for a location"""
    try:
        location = db.query(Location).filter(Location.id == location_id).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        owner_id = user_id or location.owner_id
        
        insights = ComplementaryProductsAnalyzer.get_location_insights(
            db, location_id, owner_id, days
        )
        
        return insights
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
