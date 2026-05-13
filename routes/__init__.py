"""
API Routes for the business management system
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional

from database import get_db
from models import User
from schemas import (
    UserRegister, UserLogin, UserResponse, TokenResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    SaleCreate, SaleResponse,
    CustomerCreate, CustomerUpdate, CustomerResponse,
    LocationCreate, LocationUpdate, LocationResponse,
    AnalyticsResponse, DashboardMetrics,
    BusinessInsightResponse, PredictionResponse
)
from utils import (
    hash_password, verify_password, create_access_token,
    decode_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from services import AnalyticsService, MLPredictionService, InsightService


# Create routers
auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])
products_router = APIRouter(prefix="/api/products", tags=["Products"])
sales_router = APIRouter(prefix="/api/sales", tags=["Sales"])
customers_router = APIRouter(prefix="/api/customers", tags=["Customers"])
locations_router = APIRouter(prefix="/api/locations", tags=["Locations"])
public_router = APIRouter(prefix="/api/public", tags=["Public"])
analytics_router = APIRouter(prefix="/api/analytics", tags=["Analytics"])
insights_router = APIRouter(prefix="/api/insights", tags=["Insights"])


# ==================== Authentication Routes ====================
@auth_router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        business_name=user_data.business_name,
        business_type=user_data.business_type
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user_data.location:
        from models import Location
        new_location = Location(
            owner_id=new_user.id,
            name=user_data.location.name,
            latitude=user_data.location.latitude,
            longitude=user_data.location.longitude,
            formatted_address=user_data.location.formatted_address,
            city=user_data.location.city,
            province_state=user_data.location.province_state,
            region=user_data.location.region,
            description=user_data.location.description,
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
    
    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": new_user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(new_user)
    }


@auth_router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Generate token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }


@auth_router.get("/me", response_model=UserResponse)
def get_current_user(token: str, db: Session = Depends(get_db)):
    """Get current user info"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)


# ==================== Products Routes ====================
@products_router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, token: str, db: Session = Depends(get_db)):
    """Create a new product"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Product
    new_product = Product(
        owner_id=user_id,
        **product.dict()
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return ProductResponse.from_orm(new_product)


@products_router.get("/", response_model=List[ProductResponse])
def list_products(token: str, db: Session = Depends(get_db)):
    """List all products for current user"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Product
    products = db.query(Product).filter(Product.owner_id == user_id).all()
    
    return [ProductResponse.from_orm(p) for p in products]


@products_router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, token: str, db: Session = Depends(get_db)):
    """Get a specific product"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Product
    product = db.query(Product).filter(
        (Product.id == product_id) & (Product.owner_id == user_id)
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse.from_orm(product)


@products_router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, token: str, db: Session = Depends(get_db)):
    """Update a product"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Product
    product = db.query(Product).filter(
        (Product.id == product_id) & (Product.owner_id == user_id)
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    
    return ProductResponse.from_orm(product)


@products_router.delete("/{product_id}")
def delete_product(product_id: int, token: str, db: Session = Depends(get_db)):
    """Delete a product (soft delete)"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Product
    product = db.query(Product).filter(
        (Product.id == product_id) & (Product.owner_id == user_id)
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
    
    return {"message": "Product deleted successfully"}


# ==================== Location Routes ====================
@locations_router.post("/", response_model=LocationResponse)
def create_location(location_data: LocationCreate, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    from models import Location

    new_location = Location(owner_id=user_id, **location_data.dict())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return LocationResponse.from_orm(new_location)


@locations_router.get("/", response_model=List[LocationResponse])
def list_locations(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    from models import Location

    locations = db.query(Location).filter(Location.owner_id == user_id).all()
    return [LocationResponse.from_orm(loc) for loc in locations]


@locations_router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    from models import Location

    location = db.query(Location).filter(
        (Location.id == location_id) & (Location.owner_id == user_id)
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return LocationResponse.from_orm(location)


@locations_router.put("/{location_id}", response_model=LocationResponse)
def update_location(location_id: int, location_data: LocationUpdate, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    from models import Location

    location = db.query(Location).filter(
        (Location.id == location_id) & (Location.owner_id == user_id)
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    for key, value in location_data.dict(exclude_unset=True).items():
        setattr(location, key, value)

    db.commit()
    db.refresh(location)

    return LocationResponse.from_orm(location)


@locations_router.delete("/{location_id}")
def delete_location(location_id: int, token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")
    from models import Location

    location = db.query(Location).filter(
        (Location.id == location_id) & (Location.owner_id == user_id)
    ).first()

    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    db.delete(location)
    db.commit()

    return {"message": "Location deleted successfully"}


# ==================== Sales Routes ====================
@sales_router.post("/", response_model=SaleResponse)
def create_sale(sale_data: SaleCreate, token: str, db: Session = Depends(get_db)):
    """Create a new sale"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Sale, SalesItem, Product, Location

    if sale_data.location_id is not None:
        location = db.query(Location).filter(
            (Location.id == sale_data.location_id) & (Location.owner_id == user_id)
        ).first()
        if not location:
            raise HTTPException(status_code=404, detail="Location not found for this user")

# Calculate totals and verify product data
    total_amount = 0
    total_cost = 0
    sale_items_details = []

    for item in sale_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {product.name}"
            )

        amount = item.quantity * item.unit_price
        cost = item.quantity * product.cost_price
        total_amount += amount
        total_cost += cost

        sale_items_details.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "cost_price": product.cost_price,
            "subtotal": amount,
            "product": product,
        })
    
    profit = total_amount - total_cost
    
    # Create sale
    new_sale = Sale(
        owner_id=user_id,
        customer_id=sale_data.customer_id,
        location_id=sale_data.location_id,
        total_amount=total_amount,
        total_cost=total_cost,
        profit=profit,
        payment_method=sale_data.payment_method,
        notes=sale_data.notes
    )
    
    db.add(new_sale)
    db.flush()
    
    # Add sale items and update inventory
    for item in sale_items_details:
        sales_item = SalesItem(
            sale_id=new_sale.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            cost_price=item["cost_price"],
            subtotal=item["subtotal"]
        )
        db.add(sales_item)
        
        # Update product quantity
        item["product"].quantity -= item["quantity"]
    
    db.commit()
    db.refresh(new_sale)
    
    return SaleResponse.from_orm(new_sale)


@sales_router.get("/", response_model=List[SaleResponse])
def list_sales(token: str, db: Session = Depends(get_db)):
    """List all sales for current user"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    from models import Sale
    sales = db.query(Sale).filter(Sale.owner_id == user_id).order_by(Sale.created_at.desc()).all()
    
    return [SaleResponse.from_orm(s) for s in sales]


# ==================== Public Market Routes ====================
@public_router.get("/businesses")
def list_public_businesses(
    category: Optional[str] = None,
    region: Optional[str] = None,
    min_revenue: Optional[float] = None,
    max_revenue: Optional[float] = None,
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Return public-facing business location summaries."""
    data = AnalyticsService.get_public_business_summaries(
        db,
        category=category,
        min_revenue=min_revenue,
        max_revenue=max_revenue,
        region=region,
        limit=limit,
    )
    start = max(0, (page - 1) * limit)
    return {
        "page": page,
        "limit": limit,
        "total": len(data),
        "businesses": data[start : start + limit],
    }


@public_router.get("/businesses/nearby")
def get_nearby_businesses(
    latitude: float,
    longitude: float,
    radius_km: float = 20.0,
    db: Session = Depends(get_db),
):
    """Search nearby public businesses using simple geo bounds."""
    degree_radius = radius_km / 111.0
    from models import Location

    nearby = db.query(Location).filter(
        Location.latitude.between(latitude - degree_radius, latitude + degree_radius),
        Location.longitude.between(longitude - degree_radius, longitude + degree_radius),
    ).order_by(Location.total_sales.desc()).all()

    return [
        {
            "id": loc.id,
            "name": loc.name,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "formatted_address": loc.formatted_address,
            "city": loc.city,
            "province_state": loc.province_state,
            "region": loc.region,
            "total_sales": float(loc.total_sales or 0),
        }
        for loc in nearby
    ]


@public_router.get("/heatmap")
def get_heatmap(db: Session = Depends(get_db)):
    """Return heatmap points for the public market page."""
    return AnalyticsService.get_area_heatmap(db)


@public_router.get("/insights")
def get_public_insights(db: Session = Depends(get_db)):
    """Return public-facing AI market opportunity suggestions."""
    return AnalyticsService.get_public_opportunities(db)


@public_router.get("/trending-products")
def get_public_trending_products(db: Session = Depends(get_db)):
    """Return trending product categories and demand signals."""
    return AnalyticsService.get_trending_products(db, limit=10)


# ==================== Analytics Routes ====================
@analytics_router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard(token: str, db: Session = Depends(get_db)):
    """Get complete dashboard metrics"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    metrics = AnalyticsService.get_dashboard_metrics(db, user_id)
    
    return DashboardMetrics(
        total_sales=metrics.get("monthly", {}).get("total_sales", 0),
        total_profit=metrics.get("monthly", {}).get("total_profit", 0),
        total_revenue=metrics.get("monthly", {}).get("total_revenue", 0),
        profit_margin=metrics.get("monthly", {}).get("profit_margin", 0),
        avg_transaction_value=metrics.get("monthly", {}).get("average_transaction", 0),
        total_products=metrics.get("total_products", 0),
        low_stock_products=metrics.get("low_stock_products", 0),
        top_products=metrics.get("top_products", []),
        worst_products=metrics.get("worst_products", []),
        period="monthly"
    )


# ==================== Insights Routes ====================
@insights_router.get("/", response_model=List[BusinessInsightResponse])
def get_insights(token: str, db: Session = Depends(get_db)):
    """Get business insights"""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("user_id")
    
    # Generate fresh insights
    InsightService.generate_insights(db, user_id)
    
    insights = InsightService.get_recent_insights(db, user_id, 10)
    
    return [BusinessInsightResponse.from_orm(i) for i in insights]


# Include routers in main app
def include_routes(app):
    """Include all routers in the FastAPI app"""
    app.include_router(auth_router)
    app.include_router(products_router)
    app.include_router(sales_router)
    app.include_router(customers_router)
    app.include_router(locations_router)
    app.include_router(public_router)
    app.include_router(analytics_router)
    app.include_router(insights_router)
    
    # Import and include receipts & recommendations router
    from routes.receipts_recommendations import router as receipts_router
    app.include_router(receipts_router)
